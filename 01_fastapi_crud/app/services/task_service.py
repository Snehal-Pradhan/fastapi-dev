from pathlib import Path
from app.csv_helper import read_csv, overwrite_csv
from app.models.schemas import TaskCreate, TaskUpdate
from app.exceptions import CSVError

file_path = Path(__file__).parent.parent / "database" / "tasks.csv"

try:
    tasks = read_csv(file_path)
except FileNotFoundError:
    raise CSVError(f"CSV file not found at {file_path}")
except Exception as e:
    raise CSVError(f"CSV read/write error: {e}")

def get_all_tasks():
    return tasks

def get_task_by_id(task_id: int):
    return tasks.get(task_id)

def create_task(task: TaskCreate):
    tasks[task.id] = task.model_dump()
    try:
        overwrite_csv(file_path, tasks)
    except Exception as e:
        raise CSVError(f"Failed to write to CSV: {e}")
    return tasks[task.id]

def update_task(task_id: int, updated_task: TaskCreate):
    tasks[task_id] = updated_task.model_dump()
    try:
        overwrite_csv(file_path, tasks)
    except Exception as e:
        raise CSVError(f"Failed to write to CSV: {e}")
    return tasks[task_id]

def patch_task(task_id: int, update_data: TaskUpdate):
    tasks[task_id].update(update_data)
    try:
        overwrite_csv(file_path, tasks)
    except Exception as e:
        raise CSVError(f"Failed to write to CSV: {e}")
    return tasks[task_id]

def delete_task(task_id: int):
    del tasks[task_id]
    try:
        overwrite_csv(file_path, tasks)
    except Exception as e:
        raise CSVError(f"Failed to write to CSV: {e}")
    return {"task_id": task_id}
