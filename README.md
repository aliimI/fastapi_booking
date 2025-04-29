# FastAPI Booking App
Booking backend functionality built with FastAPI, designed to be clean, scalable, and production-ready. It supports full authentication, background task processing, admin panel integration, and includes a minimal frontend via Jinja2 for basic UI interaction.

## Project architecture
### Auth API
* __registration__
* __authorization__
* __authentication__ (JWT Tokens)

### Hotels API
* __getting hotels__ (Request caching)
* __GET, POST, PUT, PATCH, DELETE methods__
* __business logic layer__
* __database work layer__

### Booking API
* __room booking__
* __error handling__

### File API
* __Hotel image uploading__ (celery background tasks)

## Features
* __JWT-based Auth__ — secure login/registration via JSON Web Tokens
* __PostgreSQL Database__ — structured using SQLAlchemy ORM and Alembic for migrations
* __Clean Architecture__ — layered structure (models, schemas, DAO, routers)
* __Background Tasks with Celery and Redis__:
  * Email confirmation on successful room booking
  * Automatic image resolution processing
* __Unit and Integration Testing__
* __Admin panel__ - using SQLAdmin
* __Mini Frontend__ - rendered pages using Jinja2 templates

## Database Schema
* Users (with secure password hashing)
* Hotels
* Rooms (each tied to a Hotel)
* Bookings (associating users and rooms with date ranges)
* Image processing (via image_id fields)
