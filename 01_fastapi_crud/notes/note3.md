

# **CRUD – C-R-D**

## **1️⃣ Create (C)**

**Purpose:** Add a new object to your database (or in-memory list).

**Syntax Example:**

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

users = []

class User(BaseModel):
    id: int
    name: str
    age: int

@app.post("/users")
def create_user(user: User):
    users.append(user)
    return {"message": "User created", "user": user}
```

**Semantics:**

* `@app.post("/users")` → defines **POST endpoint** for creating resource.
* `user: User` → FastAPI **validates request body** against the `User` model automatically.
* `users.append(user)` → stores the new user in DB/list.
* `return {...}` → returns confirmation + object.

---

## **2️⃣ Read (R)**

**Purpose:** Retrieve object(s) from the database.

**Syntax Example:**

```python
@app.get("/users")
def list_users():
    return {"users": users}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return {"message": "User found", "user": user}
    return {"message": "User not found"}
```

**Semantics:**

* `@app.get("/users")` → GET all users.
* `@app.get("/users/{user_id}")` → GET specific user by ID.
* `user_id: int` → **path parameter** automatically parsed & validated.
* Loop over DB to find object.
* Return object if found; else return message “not found”.

---

## **3️⃣ Delete (D)**

**Purpose:** Remove object from the database.

**Syntax Example:**

```python
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            users.pop(i)
            return {"message": "User deleted", "user_id": user_id}
    return {"message": "User not found"}
```

**Semantics:**

* `@app.delete("/users/{user_id}")` → DELETE HTTP method.
* Loop finds object by ID.
* `users.pop(i)` → removes object from list.
* Return confirmation message.

---

### ✅ Summary (C, R, D)

| CRUD       | HTTP Method | Endpoint      | Input       | Action         | Return              |
| ---------- | ----------- | ------------- | ----------- | -------------- | ------------------- |
| Create     | POST        | `/users`      | User (body) | Append to DB   | Confirmation + User |
| Read (all) | GET         | `/users`      | None        | Return list    | Users list          |
| Read (one) | GET         | `/users/{id}` | Path param  | Find object    | User + message      |
| Delete     | DELETE      | `/users/{id}` | Path param  | Remove from DB | Confirmation + ID   |

---