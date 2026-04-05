# Finance Backend System

## Overview
This is a backend system for managing financial records with role based access control.

## Tech Stack
- Python
- FastAPI
- SQLite
- SQLAlchemy

## Features
- User management with roles (Admin, Analyst, Viewer)
- Financial record CRUD operations
- Role based access control
- Dashboard summary APIs
- Input validation and error handling

## Project Structure

finance-backend/

├── main.py        # API routes

├── models.py      # Database models

├── schemas.py     # Request/response validation

├── database.py    # DB connection

├── requirements.txt

## API Endpoints

### Users
- POST /users → Create user
- GET /users → Get all users

### Records
- POST /records → Create record (Admin only)
- GET /records → View records
- PUT /records/{id} → Update record (Admin only)
- DELETE /records/{id} → Delete record (Admin only)

### Summary
- GET /summary → Income, expense, balance
- GET /summary/category → Category-wise totals
- GET /summary/recent → Recent transactions
- GET /summary/monthly → Monthly trends

## Access Control
- Admin → Full access
- Analyst → Read-only
- Viewer → Read-only

## API Documentation

Interactive API docs available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📥 Sample Request

POST /records

{
  "amount": 5000,
  "type": "income",
  "category": "salary",
  "date": "2026-04-04",
  "notes": "Monthly salary"
}

## Assumptions
- Authentication is simulated using `user_id` query parameter

## How to Run on localhost
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## 🌐 Live API

-> https://finance-backend-system-nqhh.onrender.com/docs
-> https://finance-backend-system-nqhh.onrender.com/redoc

## Demo Flow

1. Create an Admin User using POST /users  
2. Create financial records using POST /records  
3. Fetch all records using GET /records  
4. Filter records using GET /records/filter  
5. View analytics using:
   - GET /summary
   - GET /summary/category
   - GET /summary/monthly  

Note: Role-based restrictions apply for create/update/delete operations.

## Design Approach

The system is designed with separation of concerns using models, schemas, and database layers. Role based access control is implemented at the API level to ensure secure and structured data operations.

## Future Improvement

Modularizing routes and adding service layer for scalability.