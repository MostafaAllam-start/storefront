# Storefront

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Development](#development)
---

## Introduction

**Storefront** is a Django-based application designed to serve as a backend for e-commerce or similar data-driven web applications. It integrates a variety of tools and DRF to provide robust RESTful APIs, authentication, and asynchronous task handling.

---

## Features

- **Django REST Framework**: API endpoints for handling data.
- **JWT Authentication**: Secure login and token-based authentication using `djoser` and `djangorestframework-simplejwt`.
- **Task Scheduling and Execution**: Powered by Celery and Redis.
- **Image Handling**: Support for processing and storing images with `Pillow`.
- **Database Support**: Uses MySQL for robust data storage.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MostafaAllam-start/storefront
   cd storefront
2. Install dependencies using pipenv:
   ```bash
   pipenv install
3-Set up the environment variables:
  - **Create a .env file in the root directory with the following keys:**
     ```makefile
        DJANGO_SECRET_KEY=<your_secret_key>
        DATABASE_URL=<your_database_url>
        REDIS_URL=<your_redis_url>
4-Apply database migrations:
  ```bash
    python manage.py migrate
  ```
5-Run the development server:
  ```bash
    python manage.py runserver
  ```

---

## Usage
  - **Access the development server at http://127.0.0.1:8000/.**
  - **Use the Django admin panel for administrative tasks.**
  - **Access the API documentation via an interactive browser interface (swagger) or by using postman.**

---

## Configuration
-**Environment Variables: Stored in the .env file, including database and Redis URLs.**
-**Celery: Configure the Celery workers using the provided celerybeat-schedule.**

---
## Dependencies
- **Core Dependencies**
  - django
  - djangorestframework
  - mysqlclient
  - pillow
  - redis
  - celery

- **Authentication**
  - djoser
  - djangorestframework-simplejwt
- **Development Tools**
  - pytest
  - pytest-django
  - model-bakery
  - locust (for application performce testing)

---

## Development
1- Run tests:
  ```bash
    pytest
  ```
2- Use pytest-watch for continuous test execution during development:
  ```bash
  ptw
  ```

---



