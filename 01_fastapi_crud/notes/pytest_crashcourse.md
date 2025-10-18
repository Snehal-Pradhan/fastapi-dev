
# 🧪 Pytest + FastAPI Testing 


## 🎯 Objective

- Understand how testing works in FastAPI using `pytest`  
- Focus on **why things work** (semantics) before memorizing syntax  
- Learn project setup, test writing, and execution  
- Recognize the type of testing being done  

---

## 1️⃣ Testing Basics — Semantics

### What is testing?

> Testing is **verifying that your code behaves as expected**.  
> In FastAPI, it means checking that your API routes return the correct **status codes** and **JSON responses**.

### Types of tests relevant here:

| Type | Scope | Focus | Example |
|------|-------|-------|---------|
| **Unit Test** | Single function | Logic inside function | Test `def add(a,b)` |
| **Integration / Functional Test** | Multiple components together | API endpoint, FastAPI internals | `client.get("/users/1")` |
| **End-to-End (E2E) Test** | Full system including frontend, DB, network | Full flow of a user | Browser or Postman test |

> ✅ What we are doing here = **Integration / Functional testing**  
> We test the **route behavior**, not isolated functions.


### Why testing is important (semantics)

1. **Predictability:** Ensures API behaves consistently.  
2. **Regression safety:** Detects bugs when code changes.  
3. **Documentation:** Tests act as live examples of API behavior.  
4. **Confidence for deployment:** Passing tests = low risk in production.

## 2️⃣ Project Setup for FastAPI Testing

```

01_fastapi_crud/
├── main.py          # FastAPI app with routes
├── requirements.txt
├── pytest.ini       # Pytest configuration
└── tests/
└── test_users.py

````

- `tests/` folder → All test files reside here  
- Test files → Start with `test_*.py`  
- Test functions → Start with `test_*()`  


## 3️⃣ Dependencies

- **FastAPI** → The web framework  
- **pytest** → Python testing framework  
- **httpx** → Simulates HTTP requests in `TestClient`

Install:

```bash
pip install fastapi httpx pytest
````

> Important: `httpx` does not automatically come with base FastAPI install; it’s required for `TestClient`.


## 4️⃣ Pytest Configuration

**pytest.ini** — tells pytest where to find tests and how to run them:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = -v --maxfail=2 --disable-warnings
```

**Semantics:**

* `testpaths` → pytest scans these directories
* `python_files` → only files matching this pattern are collected
* `addopts` → additional options for verbose output, early stop, etc.


## 5️⃣ Writing Your First Test — Semantics First

### Test Concept

* `TestClient(app)` → Simulates an HTTP client internally
* `assert` → Checks a condition. Passes if true, fails if false.
* We check **status codes** and **JSON responses** → functional correctness

### Example: `tests/test_users.py`

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_user_not_found():
    # Call the route with an invalid ID
    response = client.get("/users/1")
    
    # Assert expected HTTP status
    assert response.status_code == 404
    
    # Assert expected JSON response
    assert response.json() == {"detail": "User not found"}

def test_user_found():
    response = client.get("/users/42")
    assert response.status_code == 200
    assert response.json() == {"id": 42, "name": "The Answer"}
```

**Semantics:**

* `response` object = result of simulated HTTP call
* `response.status_code` = HTTP status returned by FastAPI route
* `response.json()` = parsed JSON payload
* `assert` expresses **truth claims**: “I expect this to be true”


## 6️⃣ Running Tests — Semantics

```bash
pytest -v
```

* Pytest auto-discovers test files and functions
* Runs them **in isolation**
* Marks **pass** or **fail** based on `assert` results

**Optional commands:**

```bash
pytest tests/test_users.py -v          # Run specific file
pytest -v -k test_user_not_found       # Run specific test function
```

**What happens internally:**

1. Pytest collects all test functions
2. Calls them one by one
3. Evaluates `assert` statements
4. Reports results with context

## 7️⃣ Understanding `assert` — Semantics

* `assert condition` → check if `condition` is True
* If **True**, test continues
* If **False**, test fails and pytest reports an error

Example:

```python
assert response.status_code == 404
```

* ✅ Test passes if route returns 404
* ❌ Test fails if route returns something else

> Pytest does **not know your logic** automatically — you must express all expectations via `assert`.


## 8️⃣ Common Issues and Fixes

### Import Errors

* `ModuleNotFoundError: No module named 'crud'`
* Cause: Python cannot find your module in `sys.path`
* Fix:

  1. Run pytest from **project root**, not inside `tests/`
  2. Add project root to `sys.path` in test (temporary for small projects)

  ```python
  import sys, os
  sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
  ```

  3. Better long-term: Organize project as a package

  ```
  01_fastapi_crud/
  ├── app/
  │   ├── __init__.py
  │   └── crud.py
  └── tests/
  ```

### Missing httpx

* Install with:

```bash
pip install httpx
```

* Required for `TestClient`



## 9️⃣ Mental Model / Semantics Summary

* **TestClient** = simulate HTTP requests internally
* **assert** = express expected truth
* **pytest** = discovers tests, runs them, reports results
* **Tests don’t guess logic** = you must write all expectations explicitly
* **Running tests** from project root ensures imports resolve correctly
* **Integration / Functional testing** = testing route + FastAPI + responses, not just isolated functions


## 🔑 Key Takeaways

* Write **small, isolated test functions**
* Always **assert both status code and JSON response**
* Organize project for clean imports
* Run tests from **root folder**
* Install **httpx** for TestClient
* Pytest is **simple but powerful** — focus on **expressing expectations clearly**


