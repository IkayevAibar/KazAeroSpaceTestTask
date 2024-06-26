
# Fitness Schedule Project

This project is a web application for managing a fitness gym schedule. It is developed using Django and Django REST Framework.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/IkayevAibar/fitness_schedule_project.git
   ```
2. Navigate to the project directory:

   ```bash
   cd fitness_schedule_project
   ```
3. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/MacOS
   venv\Scripts\activate      # For Windows
   ```
4. Install dependencies:

   ```bash
   pip install -r req.txt
   ```
5. Apply migrations:

   ```bash
   python manage.py migrate
   ```

## Usage

To run the Django development server, execute the following command:

```bash
python manage.py runserver
```


After that, the application will be available at [http://127.0.0.1:8000/]().

## API

The API is available at: [http://127.0.0.1:8000/api/]()

API documentation is available at: [http://127.0.0.1:8000/swagger/]()

### Postman Integration

- You can import the OpenAPI schema into Postman for testing by [clicking here](http://127.0.0.1:8000/swagger/?format=openapi).

## Deployment with Docker

This project can also be deployed using Docker. Simply execute the following commands:

```bash
docker build -t fitness_schedule_project .
docker run -p 8000:8000 fitness_schedule_project
```

## Populating the Database with Sample Data

To populate the database with sample data, you can use the custom management command `populate_db`. This command creates sample gyms, users (both clients and trainers), schedules, and bookings for demonstration purposes.

Before running the command, ensure that you have created a superuser. The superuser, by default, has the role of admin, which allows them to perform administrative tasks in the application.

To create a superuser, use the following command:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter the superuser's email address, password, and other optional information.

Once you have created the superuser, you can then run the `populate_db` command to populate the database with sample data.

To run the command, use the following syntax:

```bash
python manage.py populate_db
```

This command will populate the database with sample data, including gyms, users, schedules, and bookings, providing you with a starting point for testing and development.

# Fitness API Documentation

This documentation provides information about the endpoints available in the Fitness API.

## Introduction

The Fitness API allows clients to manage gym schedules, bookings, trainers, and users.

## Authentication

The API uses Token-based authentication. Clients need to obtain a token by providing valid credentials. To obtain an access token for the API, send a POST request to `/api/token/` with the user's email address and password in the request body. Example request body:

```json
{
  "email": "example@example.com",
  "password": "examplePassword"
}

```

The response will contain an access token (`access`) and a refresh token (`refresh`). The access token should be included in the request header in the format `Authorization: Bearer <access_token>` to access protected endpoints.

## Endpoints

* **GET /api/bookings/**
  Description: Retrieve a list of gym bookings.
* **GET /api/bookings/get_own_bookings/**
  Description: Retrieve all booked schedules for the authenticated client.
* **GET /api/bookings/{id}/**
  Description: Retrieve details of a specific booking.
* **GET /api/schedules/**
  Description: Retrieve a list of gym schedules.
* **POST /api/schedules/create_schedule/**
  Description: Create a new gym schedule. Only accessible for trainers.
* **GET /api/schedules/get_own_schedule/**
  Description: Retrieve all schedules for the authenticated trainer.
* **GET /api/schedules/{id}/**
  Description: Retrieve details of a specific schedule.
* **POST /api/schedules/{id}/add_this_schedule/**
  Description: Book a specific schedule. Only accessible for clients.
* **POST /api/users/register/**
  Description: Register a new client.
* **POST /api/users/registerTrainer/**
  Description: Register a new trainer. Only accessible for admins.
* **GET /api/users/**
  Description: Retrieve a list of users.
* **GET /api/users/{id}/**
  Description: Retrieve details of a specific user.

## Response Formats

Responses are returned in JSON format.


# Additional Information:

1. By default, SQLite3 database is used. If you need to use another database, you can configure it in the Django settings file (`settings.py`).
2. The Gym model does not have endpoints, and creating them is not provided through the API. If you need to create Gym objects, you can do so through the Django administrative interface.
3. Some requests, such as creating a user with a trainer role, require an admin role. Make sure you are logged in as a superuser to perform such actions.
4. All functionality has been manually tested, but errors may still be encountered. If you find a bug, please report it so that i can fix it.
