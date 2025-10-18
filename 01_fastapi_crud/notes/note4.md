

# **CRUD - Update (PATCH & PUT)**

## **1️⃣ PUT – Complete Update**

**Purpose:** Replace the entire existing object with a new one.

**Syntax Example:**

```python
@app.put("/users/{user_id}")
def update_user_full(user_id: int, updated_user: User):
    for i, user in enumerate(users):
        if user.id == user_id:
            users[i] = updated_user
            return {"message": "User fully updated", "user": users[i]}
    return {"message": "User not found"}
```

**Semantics:**

* `@app.put("/users/{user_id}")` → PUT indicates **full replacement**.
* `updated_user: User` → all fields must be provided; FastAPI validates input.
* Replace existing object in DB/list with the new object.
* Return confirmation + updated object.
* Not found → return “User not found” (later we’ll improve with HTTPException).


## **2️⃣ PATCH – Partial Update**

**Purpose:** Update **only the fields provided** by the client; other fields remain unchanged.

**Why a separate model?**

* `User` model requires all fields → cannot use for PATCH.
* `UserUpdate` uses **Optional fields** → user can send only fields they want to change.

**Syntax Example:**

```python
class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None

@app.patch("/users/{user_id}")
def update_user_partial(user_id: int, user_update_data: UserUpdate):
    for user in users:
        if user.id == user_id:
            update_fields = user_update_data.dict(exclude_unset=True)
            for key, value in update_fields.items():
                setattr(user, key, value)
            return {"message": "User updated", "user": user}
    return {"message": "User not found"}
```

**Semantics:**

* `@app.patch("/users/{user_id}")` → PATCH indicates **partial update**.
* `UserUpdate` model → all fields are optional (`Optional[]`)
* `.dict(exclude_unset=True)` → include **only fields sent by the client**
* `setattr(user, key, value)` → dynamically update the object
* Other fields in object remain unchanged

---

### ✅ Summary (Update)

| Update Type    | HTTP Method | Model        | Action                      | Key Points                                              |
| -------------- | ----------- | ------------ | --------------------------- | ------------------------------------------------------- |
| Full Update    | PUT         | `User`       | Replace object              | Requires all fields; overwrites existing object         |
| Partial Update | PATCH       | `UserUpdate` | Update only provided fields | Optional fields; use `exclude_unset=True` and `setattr` |

---

