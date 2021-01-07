from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from db.db_connection import Base, engine

class InventoryInDB(Base): 
    __tablename__="inventory"
    id = Column(Integer, primary_key=True, autoincrement = True)
    name = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    discount = Column(Integer)
    total_price = Column(Integer)
Base.metadata.create_all(bind=engine)