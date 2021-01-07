from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from db.db_connection import get_db
from db.customer_db import CustomerInDB
from db.inventory_db import InventoryInDB
from models.customer_models import CustomerIn, CustomerOut, CustomerUpdateIn
from models.inventory_models import InventoryIn, InventoryOut

router = APIRouter()

## Peticiones de Customer 

@router.post("/customer/auth/")
async def auth_customer(customer_in: CustomerIn, db:Session=Depends(get_db)):
    #customer_in_db = get_customer(customer_in.username)
    customer_in_db = db.query(CustomerInDB).get(customer_in.username)
    if customer_in_db == None:
        raise HTTPException(status_code=404, detail="El cliente no existe")
    if customer_in_db.password != customer_in.password:
        raise HTTPException(status_code=403, detail="El password no es correcto")
    return {"Autenticado": True}

@router.get("/customer/fullName/{username}", response_model= CustomerOut)
async def get_fullName(username: str, db:Session=Depends(get_db)):
    #customer_in_db = get_customer(username)
    customer_in_db = db.query(CustomerInDB).get(username)
    if customer_in_db == None:
        raise HTTPException(status_code=404, detail="El cliente no existe")
    #customer_out = CustomerOut(**customer_in_db.dict())
    return customer_in_db


@router.put("/customer/transaction/")
async def make_transaction(customer_update_in: CustomerUpdateIn, db : Session=Depends(get_db)):
    #customer_update_db = get_customer(customer_update_in.username)
    customer_update_db = db.query(CustomerInDB).get(customer_update_in.username)
    if customer_update_db == None:
        raise HTTPException(status_code=404, detail="El cliente no existe")
    if customer_update_db.password != customer_update_in.password:
        return {"Autenticado": False}
    customer_update_db.address=customer_update_in.address
    customer_update_db.numberPhone=customer_update_in.numberPhone

    db.commit() 
    db.refresh(customer_update_db)
    #update_customer(customer_update_db)
    return customer_update_db