# FastAPI Project with MongoDB 

 Instructions for setting up and running a FastAPI project with MongoDB.

## Prerequisites


- Python 3.11 is used and for versions of other dependancies have a close look at requirements.txt
- MongoDB
- FastAPI and necessary Python packages (install using `pip`)
- [MongoDB Python Driver (PyMongo)](https://pymongo.readthedocs.io/en/stable/)

## Getting Started

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd fastapi-mongodb-project
   ```
2. **Install the requirements dependency in the system.**
   ```bash
    pip install -r requirements.txt

   ```
3.**Configured MongoDb**
   
   As mentioned in the assignment i have used mongoDb for thuis task and letting the shared cluster password there for testing purpose.
   ```bash
    password: abhinay
   ```
4.**Run Application**
  ```bash
  uvicorn main:app --reload
  ```
   The FastAPI application should now be running. You can access the API at http://localhost:8000.

## API Endpoints


- List All Products: GET /products/

  -Lists all available products in the system. 
- Create a New Order: POST /orders/

  -Creates a new order with a unique order ID.
- Fetch All Orders: GET /orders/

  -Fetches all orders from the system with pagination support.
- Fetch a Single Order: GET /orders/{order_id}

  -Fetches a single order by its order ID.
- Update Product Quantity: PUT /products/{product_id}

  -Updates the available quantity for a product.
- Fetch Order IDs: GET /order-ids/

  -Fetches the ObjectId of all orders.

## Sample Requests

- You can use tools like curl or API client applications (e.g., Postman) to make HTTP requests to the API endpoints.

## Project Structure

- main.py: The FastAPI application entry point.
- config.py: Configuration settings for MongoDB connection.
- models.py: Define MongoDB data models (Product, User, Order).
- schemas.py: Define data serialization and deserialization functions.
- routes.py: Define API routes and endpoints.
- requirements.txt: List of Python packages required for the project.
- data: Directory containing sample data (products.json).
- README.md: This README file.
   
