from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel
from typing import Optional,List
from database import SessionLocal
import models


app = FastAPI()

class Item(BaseModel): #serialiser
    id:int
    name:str
    description:str
    price:int
    on_offer:bool

    class Config:
        orm_mode=True

db=SessionLocal()


@app.get('/')
def index():
    return{"message":"hellooo"}

@app.get('/greet/{name}')
def greet_name(name:str):
    return {"greetings":f"hello {name}"}

@app.put('/item/{item_id}')
def update(item_id:int,item:Item):
    return{
        'name':item.name,
        'description':item.description,
        'price':item.price,
        'on_offer':item.on_offer

    }


@app.get('/items',response_model=List[Item],status_code=200)
def get_all_items():
    items=db.query(models.Item).all()

    return items

@app.get('/item/{item_id}',response_model=Item,status_code=status.HTTP_200_OK)
def get_an_item(item_id:int):
    item=db.query(models.Item).filter(models.Item.id==item_id).first()
    return item



@app.post('/items',response_model=Item,
        status_code=status.HTTP_201_CREATED)
def create_an_item(item:Item):
    db_item=db.query(models.Item).filter(models.Item.name==item.name).first()

    if db_item is not None:
        raise HTTPException(status_code=400,detail="Item already exists")



    new_item=models.Item(
        name=item.name,
        price=item.price,
        description=item.description,
        on_offer=item.on_offer
    )


    

    db.add(new_item)
    db.commit()

    return new_item



