from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from db.db_connection import get_db
from db.customer_db import CustomerInDB
from db.inventory_db import InventoryInDB
from models.customer_models import CustomerIn, CustomerOut, CustomerUpdateIn
from models.inventory_models import InventoryIn, InventoryOut
import math

router = APIRouter() 

# obtener producto del inventario
@router.get("/productos/{inventory_id}", response_model = InventoryOut)
async def inventory_get(inventory_id: int , db:Session = Depends(get_db)):
    inventory_in = db.query(InventoryInDB).get(inventory_id)
    #inventory_in = get_inventory(inventory_id) 

    if inventory_in == None: 
        raise HTTPException (status_code=404,
                detail="el producto no fue encontrado en el inventario") 
    #inventory_out = InventoryOut(**inventory_in.dict())
    return inventory_in

    # actualizar producto
@router.put("/productos/actualizar", response_model = InventoryOut)
async def product_update(inventory: InventoryIn, db:Session = Depends(get_db)): 
    inventory_in = db.query(InventoryInDB).get(inventory.id)
    #inventory_in = get_inventory(inventory.id)
    if inventory_in == None: 
        return None 
    #calculo de precio con descuento
    inventory_in.total_price = math.ceil((inventory.price/100)*(100-inventory.discount))
    # demas asignaciones
    inventory_in.price = inventory.price 
    inventory_in.quantity =  inventory.quantity
    inventory_in.discount = inventory.discount 
    #actualizacion
    #update_inventory(inventory_in)
    db.commit() 
    db.refresh(inventory_in)

    return inventory_in
    

# añadir todo lo q se encuentra inventario (with Out format)
@router.get("/productos", response_model = List)
async def all_get(db : Session = Depends(get_db)): 
    #print(type(get_all()))
    #dict_inventory = get_all()
    dict_inventory = db.query(InventoryInDB).all()
    '''
    list_out = []
    for v in  dict_inventory.values(): 
        print(type(v))
        list_out.append(InventoryOut(**v.dict()))  '''
    return dict_inventory