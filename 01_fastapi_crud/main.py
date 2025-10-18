from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id : int
    name : str
    email : str
    is_active : bool = True

@app.get("/")
def home():
    return {"message" : "home route"}

@app.get("/users/{user_id}")
def user_by_user_id(user_id:int):
    return {"user" : "present","user_id" : user_id}

@app.get("/search")
def search_by_name(user_name: str):
    return {"user" : user_name}