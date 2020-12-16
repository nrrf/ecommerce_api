import math
from db.customer_db import CustomerInDB 
from db.customer_db import get_customer, update_customer 
from db.inventory_db import InventoryInDB 
from db.inventory_db import get_inventory,update_inventory, get_all
from models.customer_models import CustomerIn, CustomerOut, CustomerUpdateIn, CustomerUpdateOut
from models.inventory_models import InventoryIn, InventoryOut


#import datetime
from fastapi import FastAPI
from fastapi import HTTPException

api = FastAPI()




api = FastAPI()

### Peticiones de Inventory 

from fastapi.middleware.cors import CORSMiddleware
origins = [
"http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
"http://localhost", "http://localhost:8080",
]
api.add_middleware(
CORSMiddleware, allow_origins=origins,
allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# obtener producto del inventario
@api.get("/productos/{inventory_id}")
async def inventory_get(inventory_id: int): 
    inventory_in = get_inventory(inventory_id) 
    if inventory_in == None: 
        raise HTTPException (status_code=404,
                detail="el producto no fue encontrado en el inventario") 
    inventory_out = InventoryOut(**inventory_in.dict())
    return inventory_out


# actualizar producto
@api.put("/productos/actualizar")
async def product_update(inventory: InventoryIn): 
    inventory_in = get_inventory(inventory.id)
    if inventory_in == None: 
        return None 
    #calculo de precio con descuento
    inventory_in.total_price = math.ceil((inventory.price/100)*(100-inventory.discount))
    # demas asignaciones
    inventory_in.price = inventory.price 
    inventory_in.quantity =  inventory.quantity
    inventory_in.discount = inventory.discount 
    #actualizacion
    update_inventory(inventory_in)
    #mapeado de salida
    inventory_out = InventoryOut(**inventory_in.dict())
    return inventory_out
    

# añadir todo lo q se encuentra inventario (with Out format)
@api.get("/productos")
async def all_get(): 
    #print(type(get_all()))
    dict_inventory = get_all()
    list_out = []
    for v in  dict_inventory.values(): 
        print(type(v))
        list_out.append(InventoryOut(**v.dict()))  
    return list_out
## Peticiones de Customer 

@api.post("/customer/auth/")
async def auth_customer(customer_in: CustomerIn):
    customer_in_db = get_customer(customer_in.username)
    if customer_in_db == None:
        raise HTTPException(status_code=404, detail="El cliente no existe")
    if customer_in_db.password != customer_in.password:
        return {"Autenticado": False}
    return {"Autenticado": True}

@api.get("/customer/fullName/{username}")
async def get_fullName(username: str):
    customer_in_db = get_customer(username)
    if customer_in_db == None:
        raise HTTPException(status_code=404, detail="El cliente no existe")
    customer_out = CustomerOut(**customer_in_db.dict())
    return customer_out


@api.put("/customer/transaction/")
async def make_transaction(customer_update_in: CustomerUpdateIn):
    customer_update_db = get_customer(customer_update_in.username)
    if customer_update_db == None:
        raise HTTPException(status_code=404, detail="El cliente no existe")
    if customer_update_db.password != customer_update_in.password:
        return {"Autenticado": False}
    customer_update_db.address=customer_update_in.address
    customer_update_db.numberPhone=customer_update_in.numberPhone
    update_customer(customer_update_db)
    return customer_update_db