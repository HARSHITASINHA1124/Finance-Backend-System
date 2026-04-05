from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import models, schemas
from typing import Optional
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy import extract

tags_metadata = [
    {"name": "Users", "description": "User management and roles"},
    {"name": "Records", "description": "Financial records operations"},
    {"name": "Summary", "description": "Dashboard analytics APIs"},
]

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Hello, World!"}
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", tags=["Users"], summary="Create a new user", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    new_user = models.User(
        name=user.name,
        email=user.email,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users", tags=["Users"], summary="Get all users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.post("/records", tags=["Records"], summary="Create a new financial record (Admin only)",description="Allows admin users to create income or expense records.", response_model=schemas.RecordResponse)
def create_record(record: schemas.RecordCreate,user_id: int, db: Session = Depends(get_db)):
    user = get_current_user(user_id, db)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")
    new_record = models.FinancialRecord(
        amount=record.amount,
        type=record.type,
        category=record.category,
        date=record.date,
        notes=record.notes
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


@app.get("/records", tags=["Records"], summary="Get all financial records")
def get_records(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.FinancialRecord).offset(skip).limit(limit).all()


@app.get("/records/filter",tags=["Records"], summary="Filter records", response_model=list[schemas.RecordResponse])
def filter_records(
    type: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.FinancialRecord)
    if type:
        query = query.filter(models.FinancialRecord.type == type)
    if category:
        query = query.filter(models.FinancialRecord.category == category)
    return query.all()


@app.put("/records/{record_id}")
def update_record(
    record_id: int,
    record: schemas.RecordCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    user = get_current_user(user_id, db)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")
    db_record = db.query(models.FinancialRecord).filter(models.FinancialRecord.id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")

    db_record.amount = record.amount
    db_record.type = record.type
    db_record.category = record.category
    db_record.date = record.date
    db_record.notes = record.notes
    db.commit()
    return {"message": "Record updated"}


@app.delete("/records/{record_id}")
def delete_record(
    record_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    user = get_current_user(user_id, db)

    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")

    db_record = db.query(models.FinancialRecord).filter(models.FinancialRecord.id == record_id).first()

    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(db_record)
    db.commit()
    return {"message": "Record deleted"}


def get_current_user(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="Invalid or inactive user")
    
    return user


@app.get("/summary", tags=["Summary"], summary="Get total income, expense, balance")
def get_summary(db: Session = Depends(get_db)):
    total_income = db.query(func.sum(models.FinancialRecord.amount))\
        .filter(models.FinancialRecord.type == "income").scalar() or 0
    total_expense = db.query(func.sum(models.FinancialRecord.amount))\
        .filter(models.FinancialRecord.type == "expense").scalar() or 0
    balance = total_income - total_expense
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance
    }


@app.get("/summary/category", tags=["Summary"], summary="Get summary by category")
def category_summary(db: Session = Depends(get_db)):
    results = db.query(
        models.FinancialRecord.category,
        func.sum(models.FinancialRecord.amount)
    ).group_by(models.FinancialRecord.category).all()

    return [
        {"category": r[0], "total": r[1]}
        for r in results
    ]


@app.get("/summary/recent")
def recent_transactions(db: Session = Depends(get_db)):
    records = db.query(models.FinancialRecord)\
        .order_by(models.FinancialRecord.date.desc())\
        .limit(5).all()

    return records


@app.get("/summary/monthly")
def monthly_summary(db: Session = Depends(get_db)):
    results = db.query(
        extract('month', models.FinancialRecord.date),
        func.sum(models.FinancialRecord.amount)
    ).group_by(extract('month', models.FinancialRecord.date)).all()

    return [
        {"month": int(r[0]), "total": r[1]}
        for r in results
    ]