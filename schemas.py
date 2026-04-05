from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Literal

class UserCreate(BaseModel):
    name: str = Field(example="John Doe")
    email: EmailStr = Field(example="john_doe@gmail.com")
    role: Literal["admin", "analyst", "viewer"] = Field(example="admin")  # admin / analyst / viewer

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class RecordCreate(BaseModel):
    amount: float = Field(gt=0, example=5000)
    type: Literal["income", "expense"] = Field(example="income")  # income / expense
    category: str = Field(example="Salary")
    date: date
    notes: str = Field(example="Monthly salary")

class RecordResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: date
    notes: str

    class Config:
        from_attributes = True