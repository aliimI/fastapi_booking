import time
import sentry_sdk

from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi_versioning import VersionedFastAPI, version
from pydantic import BaseModel
from redis import asyncio as aioredis
from sqladmin import Admin, ModelView

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.models import Users
from app.users.router import router as router_users
from fastapi import Depends, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.logger import logger


sentry_sdk.init(
    dsn="https://c7150e77a9e814db250f3e8792a6c279@o4509003867291648.ingest.de.sentry.io/4509003869651024",
    send_default_pii=True,
)



@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    
    yield

app = FastAPI(lifespan=lifespan)




app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_pages)
app.include_router(router_hotels)
app.include_router(router_images)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"]
)


app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    # description='Greet users with a nice message',
#     middleware=[
#         Middleware(SessionMiddleware, secret_key='mysecretkey')
#     ]
)


admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)



@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info("Request hadling time", extra={
        "process_time": round(process_time, 4)
    })
    return response




app.mount("/static", StaticFiles(directory="app/static"), "static")