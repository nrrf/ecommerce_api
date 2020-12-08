from pydantic import BaseModel
#from datetime import datetime

class InventoryIn(BaseModel):
    name: str
    cantidad: int

class InventoryOut(BaseModel):
    cantidad: int