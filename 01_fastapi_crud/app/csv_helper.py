import csv
from pathlib import Path

def read_csv(filename : str) -> list[dict]:
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return rows

def write_csv(filename:str,row:dict):
    with open(filename, "a", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "title", "description", "status", "due_date"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(row)
