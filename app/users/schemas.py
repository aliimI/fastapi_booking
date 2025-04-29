from pydantic import BaseModel, ConfigDict, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str
