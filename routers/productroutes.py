# routes.py
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Path, Query
from pymongo import MongoClient
from models.productmodel import Product, User, OrderItem, UserAddress, Order
from config.db import MONGODB_URL, DB_NAME
from schemas.productserializer import deserialize_order, serialize_order, serialize_product
from httpx import AsyncClient
order_id_api_url = "http://localhost:8000/orders"  #to be used in api with route orders-with-products (line no.166)

async def get_total_amount(order_id):
    async with AsyncClient() as client:
        response = await client.get(f"{order_id_api_url}/{order_id}")

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch total amount")

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
    total_price = 0  # Initialize the total price for the order

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

        # Check if product quantity is sufficient
        if item.bought_quantity > product['available_quantity']:
            error_message = f"Insufficient quantity for product with ID {product_id}. Available quantity: {product['available_quantity']}"
            print(error_message)  # Print the error for debugging
            raise HTTPException(status_code=400, detail=error_message)

        # Update the product quantity in the collection
        new_quantity = product['available_quantity'] - item.bought_quantity
        products_collection.update_one({"_id": product_id}, {"$set": {"available_quantity": new_quantity}})

        # Calculate the price for the current item and add it to the total price
        item_price = product['product_price'] * item.bought_quantity
        total_price += item_price

    # Generate a new ObjectId to use as the order ID
    order_id = ObjectId()

    # Add the order_id and total_price to the order data dictionary
    order_dict = serialize_order(order)
    order_dict["_id"] = order_id
    order_dict["total_price"] = total_price

    # Insert the order data into the orders collection
    orders_collection.insert_one(order_dict)

    # Return the order ID and total price as a response
    return {"order_id": str(order_id), "total_price": total_price}
# Fetching all orders with pagination
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

# Fetching all orders with pagination and returning the cumulative total amount of products for each order
@router.get("/order-ids/")
async def list_order_ids():
    # Retrieve all orders from the database
    orders = list(orders_collection.find({}, {"_id": 1, "items": 1}))

    # Calculate the cumulative total amount of products for each order
    order_ids = []
    for order in orders:
        order_id = str(order["_id"])  # Convert ObjectId to string

        # Calculate the cumulative total amount for this order
        total_amount = 0
        for item in order["items"]:
            product_id = item["product_id"]
            product = products_collection.find_one({"_id": ObjectId(product_id)})
            if product:
                total_amount += product["product_price"] * item["bought_quantity"]

        order_ids.append({"order_id": order_id, "total_amount_of_products": total_amount})

    return order_ids
# Delete an order by Order ID
@router.delete("/orders/{order_id}")
async def delete_order(order_id: str = Path(..., description="The ID of the order to delete")):
    try:
        bson_order_id = ObjectId(order_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid order ID: {order_id}")

    # Check if the order exists
    existing_order = orders_collection.find_one({"_id": bson_order_id})
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Delete the order
    orders_collection.delete_one({"_id": bson_order_id})

    return {"message": "Order deleted successfully"}

@router.get("/orders-with-product-details/")
async def get_orders_with_product_details():
    # Define the MongoDB aggregation pipeline
    pipeline = [
        {
            "$lookup": {
                "from": "products",  # to join with product 
                "localField": "items.product_id",  # Field from the "orders" 
                "foreignField": "_id",  # Field from the "products" 
                "as": "product_details"  # Alias 
            }
        # },
        # {
        #     "$unwind": {
        #         "path": "$product_details",
        #         "preserveNullAndEmptyArrays": True  # Preserve orders even if there are no matching products
        #     }
        # },
        # {
        #     "$group": {
        #         "_id": "$_id",  # Group by order ID
        #         "user": {"$first": "$user"},  # Preserve user information
        #         "user_address": {"$first": "$user_address"},  # Preserve user address
        #         "items": {
        #             "$push": "$items"  # Preserve items array
        #         },
        #         "total_amount": {
        #             "$sum": {
        #                 "$multiply": ["$product_details.product_price", "$items.boughtQuantity"]
        #             }  # Calculate total amount for the order
        #         }
        #     }
        }
    ]

    # Execute the aggregation query
    result = list(orders_collection.aggregate(pipeline))

    # Convert ObjectId to string in the result
    for order in result:
        order["_id"] = str(order["_id"])  # Convert ObjectId to string

    # Return the orders with product details and total amount
    return result