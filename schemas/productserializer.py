from pydantic import BaseModel
from typing import List

from models.productmodel import Order, OrderItem, Product, User, UserAddress

# ... Other schema definitions ...

# Serialization functions
def serialize_product(product: Product) -> dict:
    return {
        
        "product_name": product.product_name,
        "product_price": product.product_price,
        "available_quantity": product.available_quantity,
        
    }

def serialize_order(order: Order) -> dict:
    return {
        "user": serialize_user(order.user),
        "items": [serialize_order_item(item) for item in order.items],
        "user_address": serialize_user_address(order.user_address),
    }

# Deserialization functions
def deserialize_product(data: dict) -> Product:
    return Product(**data)

def deserialize_order(data: dict) -> Order:
    return Order(
        user=deserialize_user(data["user"]),
        items=[deserialize_order_item(item) for item in data["items"]],
        user_address=deserialize_user_address(data["user_address"]),
    )

def serialize_user(user: User) -> dict:
    return {
        "username": user.username,
        "email": user.email,
    }

def deserialize_user(data: dict) -> User:
    return User(**data)

def serialize_order_item(item: OrderItem) -> dict:
    return {
        "product_id": item.product_id,
        "bought_quantity": item.bought_quantity,
        "total_amount": item.total_amount,
    }

def deserialize_order_item(data: dict) -> OrderItem:
    return OrderItem(**data)

def serialize_user_address(address: UserAddress) -> dict:
    return {
        "city": address.city,
        "country": address.country,
        "zip_code": address.zip_code,
    }

def deserialize_user_address(data: dict) -> UserAddress:
    return UserAddress(**data)
