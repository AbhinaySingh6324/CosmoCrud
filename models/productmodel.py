# models.py
from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    product_name: str
    product_price: float
    available_quantity: int

class User(BaseModel):
    username: str
    email: str

class OrderItem(BaseModel):
    product_id: str
    bought_quantity: int
    total_amount: float

class UserAddress(BaseModel):
    city: str
    country: str
    zip_code: str

class Order(BaseModel):
    user: User
    items: List[OrderItem]
    user_address: UserAddress
