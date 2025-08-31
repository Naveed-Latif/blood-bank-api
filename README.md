# Blood Donation API

A FastAPI-based REST API for blood donation signup and management.

## Features

- User registration with validation
- User authentication (login)
- PostgreSQL database integration
- Data validation using Pydantic
- RESTful API endpoints

## Project Structure

```
app/
├── __init__.py
├── main.py          # FastAPI application and routes
├── models.py        # SQLAlchemy database models
├── schemas.py       # Pydantic request/response schemas
├── database.py      # Database configuration and session
└── config.py        # Application configuration
├── requirements.txt # Python dependencies
├── run.py          # Application runner
└── README.md       # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. PostgreSQL Database Setup

1. Install PostgreSQL on your system
2. Create a new database:
   ```sql
   CREATE DATABASE blood_donation_db;
   ```
3. Update the database URL in `app/config.py`:
   ```python
   DATABASE_URL = "postgresql://your_username:your_password@localhost:5432/blood_donation_db"
   ```

### 3. Run the Application

```bash
python run.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Root
- `GET /` - Welcome message

### Authentication
- `POST /signup` - Register new blood donor
- `POST /login` - User login

### Users
- `GET /users` - Get all registered users
- `GET /users/{user_id}` - Get specific user by ID

## API Documentation

Once the server is running, you can access:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`

## Example Usage

### Register a new user:
```bash
curl -X POST "http://localhost:8000/signup" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John",
       "last_name": "Doe",
       "phone_number": "1234567890",
       "blood_group": "A+",
       "city": "Karachi",
       "country": "Pakistan",
       "password": "SecurePass1!"
     }'
```

### Login:
```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/json" \
     -d '{
       "phone_number": "1234567890",
       "password": "SecurePass1!"
     }'
```

## Validation Rules

- **Names**: Only letters and spaces allowed
- **Phone Number**: 10-15 digits
- **Blood Group**: Must be one of A+, A-, B+, B-, AB+, AB-, O+, O-
- **Country**: Currently only Pakistan is accepted
- **Password**: 8-11 characters, must contain uppercase and special character
- **Donation Date**: Cannot be in the future 