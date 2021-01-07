from sqlalchemy import Column, Integer, String
from db.db_connection import Base, engine

class CustomerInDB(Base): 
    __tablename__ = "customer"

    username = Column(String, primary_key= True, unique=True)
    password = Column(String)
    name = Column(String)
    secondName = Column(String)
    lastname = Column(String)
    secondLastname = Column(String)
    address = Column(String)
    numberPhone = Column(Integer)

Base.metadata.create_all(bind=engine)