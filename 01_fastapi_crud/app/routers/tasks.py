from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.schemas import TaskCreate, TaskUpdate, TaskOut
from app.services.task_service import (
    get_all_tasks, get_task_by_id, create_task,
    update_task, patch_task, delete_task
)

router = APIRouter(prefix="/tasks", tags=["tasks"])

# ------------------------------
# GET /tasks - list all tasks
# ------------------------------
@router.get("/", response_model=List[TaskOut])
def read_tasks():
    # convert dict of tasks to a list for Swagger examples
    return list(get_all_tasks().values())

# ------------------------------
# GET /tasks/{id} - get task by ID
# ------------------------------
@router.get("/{id}", response_model=TaskOut)
def read_task(id: int):
    task = get_task_by_id(id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {id} not found"
        )
    return task

# ------------------------------
# POST /tasks - create new task
# ------------------------------
@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def add_task(task: TaskCreate):
    if task.id in get_all_tasks():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"id {task.id} already exists"
        )
    return create_task(task)

# ------------------------------
# PUT /tasks/{id} - replace task
# ------------------------------
@router.put("/{id}", response_model=TaskOut)
def replace_task(id: int, updated_task: TaskCreate):
    if id not in get_all_tasks():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {id} not found"
        )
    if updated_task.id != id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID in path and body must match"
        )
    return update_task(id, updated_task)

# ------------------------------
# PATCH /tasks/{id} - partial update
# ------------------------------
@router.patch("/{id}", response_model=TaskOut)
def modify_task(id: int, task_update: TaskUpdate):
    task = get_task_by_id(id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {id} not found"
        )
    update_data = task_update.model_dump(exclude_unset=True)
    return patch_task(id, update_data)

# ------------------------------
# DELETE /tasks/{id} - remove task
# ------------------------------
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def remove_task(id: int):
    task = get_task_by_id(id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {id} not found"
        )
    return delete_task(id)
