# routes.py
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query
from pymongo import MongoClient
from models.productmodel import Product, User, OrderItem, UserAddress, Order
from config.db import MONGODB_URL, DB_NAME
from schemas.productserializer import deserialize_order, serialize_order, serialize_product

# Initialize MongoDB client and database
client = MongoClient(MONGODB_URL)
db = client[DB_NAME]

# Define MongoDB collections
products_collection = db["products"]
orders_collection = db["orders"]

# Create a FastAPI router
router = APIRouter()

# Create a new product
@router.post("/products/")
async def create_product(product: Product):
    serialized_product = serialize_product(product)
    product_id = products_collection.insert_one(serialized_product).inserted_id
    return {"product_id": str(product_id)}

# List all available products
@router.get("/products/")
async def list_products():
                                                                                          # Retrieve products from the database
    products = list(products_collection.find({}))

                                                                                           # Serialize the products with product IDs
    serialized_products = [serialize_product(Product(**product)) for product in products]
    for i, product in enumerate(products):
        serialized_products[i]["_id"] = str(product["_id"])  # Convert _id to string


    return serialized_products

# Create a new order
@router.post("/orders/")
async def create_order(order: Order):
    # Check if products in the order exist in the products collection
    for item in order.items:
        product_id = item.product_id
        try:
            product_id = ObjectId(product_id)  # Convert the product_id to ObjectId
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid product ID: {product_id}")

        product = products_collection.find_one({"_id": product_id})
        if not product:
            error_message = f"Product with ID {product_id} does not exist."
            print(error_message)  # Print the error for debugging
            raise HTTPException(status_code=400, detail=error_message)

    # Generate a new ObjectId to use as the order ID
    order_id = ObjectId()

    # Add the order_id to the order data dictionary
    order_dict = serialize_order(order)
    order_dict["_id"] = order_id

    # Insert the order data into the orders collection
    orders_collection.insert_one(order_dict)

    # Return the order ID as a response
    return {"order_id": str(order_id)}

# Fetch all orders with pagination
@router.get("/orders/")
async def list_orders(limit: int = Query(10, description="Number of orders per page"), offset: int = Query(0, description="Page number")):
    orders = list(orders_collection.find({}, {"_id": 0}).skip(offset * limit).limit(limit))
    deserialized_orders = [deserialize_order(order) for order in orders]
    return deserialized_orders
# Fetch a single order by Order ID
@router.get("/orders/{order_id}")
async def get_order(order_id: str):
    try:
        bson_order_id = ObjectId(order_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid order ID: {order_id}")

    order = orders_collection.find_one({"_id": bson_order_id}, {"_id": 0})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    deserialized_order = deserialize_order(order)
    return deserialized_order

# Update product quantity by Product ID
@router.put("/products/{product_id}")
async def update_product(product_id: str, available_quantity: int):
    try:
        bson_product_id = ObjectId(product_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid product ID: {product_id}")

    result = products_collection.update_one(
        {"_id": bson_product_id},
        {"$set": {"available_quantity": available_quantity}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated successfully"}

@router.get("/order-ids/")
async def list_order_ids():
    # Retrieve all orders from the database
    orders = list(orders_collection.find({}, {"_id": 1}))

    # Extract and return the ObjectId of each order
    order_ids = [{"order_id":str(order["_id"])} for order in orders]

    return order_ids
