# FastAPI Booking App
Booking backend functionality built with FastAPI, designed to be clean, scalable, and production-ready. It supports full authentication, background task processing, admin panel integration, and includes a minimal frontend via Jinja2 for basic UI interaction.

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
