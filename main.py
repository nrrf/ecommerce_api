from fastapi import FastAPI, Depends
from fastapi import HTTPException

from routers.customer_router import router as router_customer
from routers.inventory_router import router as router_inventory

api = FastAPI()

### Peticiones de Inventory 

from fastapi.middleware.cors import CORSMiddleware
origins = [
"http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
"http://localhost", "http://localhost:8080","https://new-ecommerce-app.herokuapp.com"
]
api.add_middleware(
CORSMiddleware, allow_origins=origins,
allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

api.include_router(router_customer)
api.include_router(router_inventory)