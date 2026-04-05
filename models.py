from sqlalchemy import Column, Integer, String, Boolean, Float, Date
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    role = Column(String)  # admin / analyst / viewer
    is_active = Column(Boolean, default=True)

class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type = Column(String)  # income / expense
    category = Column(String)
    date = Column(Date, default=datetime.date.today)
    notes = Column(String)