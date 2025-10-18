import csv
from pathlib import Path

def read_csv(filename: Path):
    data = {}
    try:
        with open(filename, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row_id = int(row['id']) 
                row['id'] = row_id
                data[row_id] = row
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {filename}")
    except Exception as e:
        raise RuntimeError(f"Error reading CSV: {e}")
    return data

def overwrite_csv(filename: Path, data: dict):
    try:
        with open(filename, "w", newline="") as f:
            fieldnames = ["id", "title", "description", "status", "due_date"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data.values())
    except Exception as e:
        raise RuntimeError(f"Error writing CSV: {e}")
