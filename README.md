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
   git clone git@github.com:AbhinaySingh6324/CosmoCrud.git
   cd <Your Cloned Directory Name>
   ```
2. **Create Virtual Enviroment and Install the requirements in the Virtual Enviroment.**
    ```bash
    pip install venv
    python -m venv <nam of virtual env>
    .<name of env>/Scripts/activate  //for activating env//
    pip install -r requirements.txt

    ```
3. **Configured MongoDb**
   
   As mentioned in the assignment i have used mongoDb for thuis task and letting the shared cluster password there for testing purpose.
    ```bash
    password: abhinay
   ```
4. **Run Application**
   ```bash
   uvicorn main:app --reload
   ```
   The FastAPI application should now be running. You can access the API at http://localhost:8000.

## API Endpoints


- List All Products:
   ```bash
   GET /products/
  ```

  - Lists all available products in the system. 
- Create a New Order: POST /orders/
   ```bash
   POST /orders/
  ```
  

  - Creates a new order with a unique order ID.
- Fetch All Orders: GET /orders/
   ```bash
   GET /orders/
  ```

  - Fetches all orders from the system with pagination support.
- Fetch a Single Order:
   ```bash
  GET /orders/{order_id}
   ```

  - Fetches a single order by its order ID.
- Update Product Quantity: 
  ```bash
  PUT /products/{product_id}
   ```

  - Updates the available quantity for a product.
- Fetch Order IDs:
  ```bash
  PUT /products/{product_id}
  ```
  - Fetches the ObjectId of all orders along with their calculated amount.
- Delete Orders with Order IDs:
  ```bash
  DELETE /orders/{order_id}
  ```
  - If the order exists, it will be deleted, and you will receive a response with the message:

.

## Sample Requests

- You can use tools like curl or API client applications (e.g., Postman) to make HTTP requests to the API endpoints,FastAPI also provides swagger powered documentation and testing  at this URI once your uvicorn server is up and running.

 ```bash
  http://127.0.0.1:8000/docs
  ```
  

## Project Structure

- main.py: The FastAPI application entry point.
- config.py: Configuration settings for MongoDB connection.
- models.py: Define MongoDB data models (Product, User, Order).
- schemas.py: Define data serialization and deserialization functions.
- routes.py: Define API routes and endpoints.
- requirements.txt: List of Python packages required for the project.
- data: Directory containing sample data (products.json).
- README.md: This README file.
   
