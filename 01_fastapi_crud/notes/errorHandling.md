# Error Handling

Error handling in FastAPI is all about **predictability** and **graceful failure**. Your API should **never crash** due to an expected or unexpected error, and it should **always return structured, informative responses**.

**Goal:**

* Fail gracefully on bad inputs
* Return consistent error responses
* Separate **expected errors** from **unexpected ones**


## 1️⃣ Route-Level Errors (HTTPException)

**Purpose:** Handle **basic, expected failures** directly in route logic.

**Syntax:**

```python
from fastapi import HTTPException, status

if not user_exists:
    raise HTTPException(status_code=404, detail="User not found")
```

**Key Points:**

* Simple, minimal error reporting (`status_code + detail string`)
* Quick way to communicate predictable issues
* Response example:

```json
{"detail": "User not found"}
```

**Semantics:** Think of this as a **local safety net** for known error conditions.

---

## 2️⃣ Structured / Detailed JSON Errors

**Purpose:** Provide **richer, more informative errors** while still handling them at the route level.

**Syntax:**

```python
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={"error": "User already exists", "hint": "Try a different user ID"}
)
```

**Response Example:**

```json
{
  "error": "User already exists",
  "hint": "Try a different user ID"
}
```

**Semantics:**

* Still local to the route
* Adds context for client consumption
* Useful when you want clients to react programmatically

---

## 3️⃣ Custom Exception Classes (Domain/Business Errors)

**Purpose:** Cleanly separate **business/domain logic errors** from route logic.

**Step 1: Define Exception**

```python
class UserAlreadyExists(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
```

**Step 2: Add Handler**

```python
from fastapi.responses import JSONResponse
from fastapi import Request

@app.exception_handler(UserAlreadyExists)
async def user_exists_handler(request: Request, exc: UserAlreadyExists):
    return JSONResponse(
        status_code=400,
        content={"error": f"User with ID {exc.user_id} already exists", "hint": "Try a different user ID"}
    )
```

**Step 3: Raise in Route**

```python
if user_exists:
    raise UserAlreadyExists(user_id)
```

**Semantics:**

* Route = business logic only
* Handler = formats and returns structured response
* Scales easily for large apps with many domain errors
* Example mental model:

```
Route logic ---> raises UserAlreadyExists ---> handler formats JSON ---> client sees structured info
```

---

## 4️⃣ Global Exception Handler (Catch-All)

**Purpose:** Catch **unexpected/unhandled exceptions** and return structured JSON instead of ugly HTML or server crash.

**Syntax:**

```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "path": request.url.path
        },
    )
```

**Semantics:**

* Only triggers for **uncaught exceptions**
* Acts as the **last safety net**
* Ensures API responses remain consistent even for runtime or system errors

**Example Flow:**

```
Client Request
      │
      ▼
Route logic executes
  ├─ raise HTTPException → handled locally
  ├─ raise CustomException → handled by custom handler
  └─ uncaught Exception → handled by global handler
```

---

## 🧩 Summary Table

| Layer                       | Purpose                      | Example                     | Response                                                                             |
| --------------------------- | ---------------------------- | --------------------------- | ------------------------------------------------------------------------------------ |
| Route-level (HTTPException) | Expected, basic errors       | User not found              | {"detail": "User not found"}                                                         |
| Structured JSON             | More context at route        | Duplicate user              | {"error": "User exists", "hint": "Try a different ID"}                               |
| Custom Exception Class      | Business/domain logic errors | UserAlreadyExists           | {"error": "User with ID 1 already exists", "hint": "Try a different ID"}             |
| Global Handler              | Unexpected errors            | ZeroDivisionError, DB error | {"error": "Internal Server Error", "message": "division by zero", "path": "/divide"} |

---

## 💡 Key Mental Model

* **Route = business logic & expected errors**
* **Custom exception handler = domain-specific formatting**
* **Global handler = last line of defense for unexpected errors**

> Layered approach ensures **predictable, clean, and professional API responses**. Perfect for building production-ready FastAPI apps.

---