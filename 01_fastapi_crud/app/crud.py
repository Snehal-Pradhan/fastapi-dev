from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

users: List["User"] = []

class User(BaseModel):
    id: int
    name: str
    age: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None

@app.post("/users")
def create_user(user: User):
    users.append(user)
    return {"message": "User created", "user": user}

@app.get("/users")
def list_users():
    return {"users": users}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return {"message": "User found", "user": user}
    return {"message": "User not found"}

@app.patch("/users/{user_id}")
def update_user_partial(user_id: int, user_update_data: UserUpdate):
    for user in users:
        if user.id == user_id:
            update_fields = user_update_data.dict(exclude_unset=True)
            for key, value in update_fields.items():
                setattr(user, key, value)
            return {"message": "User updated", "user": user}
    return {"message": "User not found"}

@app.put("/users/{user_id}")
def update_user_full(user_id: int, updated_user: User):
    for i, user in enumerate(users):
        if user.id == user_id:
            users[i] = updated_user
            return {"message": "User fully updated", "user": users[i]}
    return {"message": "User not found"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            users.pop(i)
            return {"message": "User deleted", "user_id": user_id}
    return {"message": "User not found"}
