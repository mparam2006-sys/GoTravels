from pydantic import BaseModel, EmailStr
from typing import List


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str | None = None
    password: str


class PassengerCreate(BaseModel):
    full_name: str
    age: int
    gender: str
    id_type: str | None = None
    id_number: str | None = None


class PassengerList(BaseModel):
    passengers: List[PassengerCreate]