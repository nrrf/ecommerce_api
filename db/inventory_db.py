#from typing import Dict
from pydantic import BaseModel 

class InventoryInDB(BaseModel): 
    id_inventory: str
    name: str 
    cantidad: int