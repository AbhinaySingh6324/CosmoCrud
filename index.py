from fastapi import FastAPI
from routers.productroutes import router
app = FastAPI()
app.include_router(router)