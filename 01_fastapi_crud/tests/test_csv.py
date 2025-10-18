from app.csv_helper import read_csv,overwrite_csv
from pathlib import Path
import tempfile
import shutil
import csv
test_file_path = Path(__file__).parent/ "test_tasks.csv"

csv_data = [
    {'id': '1', 'title': 'Finish report', 'description': 'Complete the quarterly report', 'status': 'pending', 'due_date': '2025-10-20'},
    {'id': '2', 'title': 'Team meeting', 'description': '', 'status': 'done', 'due_date': '2025-10-18'},
    {'id': '3', 'title': 'Update website', 'description': 'Add new product info', 'status': 'pending', 'due_date': ''},
    {'id': '4', 'title': 'Client follow-up', 'description': 'Call client about feedback', 'status': 'done', 'due_date': '2025-10-19'},
    {'id': '5', 'title': 'Plan workshop', 'description': '', 'status': 'pending', 'due_date': '2025-10-25'},
    {'id': '6', 'title': 'Code review', 'description': 'Review PR #42', 'status': 'pending', 'due_date': ''},
    {'id': '7', 'title': 'Write blog post', 'description': 'Introduction to FastAPI', 'status': 'done', 'due_date': '2025-10-28'}
]

csv_dict_data = {
  1: {'id': '1', 'title': 'Finish report', 'description': 'Complete the quarterly report', 'status': 'pending', 'due_date': '2025-10-20'},
  2: {'id': '2', 'title': 'Team meeting', 'description': '', 'status': 'done', 'due_date': '2025-10-18'},
  3: {'id': '3', 'title': 'Update website', 'description': 'Add new product info', 'status': 'pending', 'due_date': ''},
  4: {'id': '4', 'title': 'Client follow-up', 'description': 'Call client about feedback', 'status': 'done', 'due_date': '2025-10-19'},
  5: {'id': '5', 'title': 'Plan workshop', 'description': '', 'status': 'pending', 'due_date': '2025-10-25'},
  6: {'id': '6', 'title': 'Code review', 'description': 'Review PR #42', 'status': 'pending', 'due_date': ''},
  7: {'id': '7', 'title': 'Write blog post', 'description': 'Introduction to FastAPI', 'status': 'done', 'due_date': '2025-10-28'}
}



def test_read_csv():
    """
    Test that read_csv correctly reads all rows from a CSV file.

    Steps:
    1. Read the test_tasks.csv file using read_csv().
    2. Compare the returned list of dictionaries to the expected CSV data.

    This ensures that read_csv preserves all columns and values correctly.
    """
    rows =  read_csv(test_file_path) 
    assert rows == csv_dict_data


def test_overwrite_csv():
    expected = {
  1: {'id': '1', 'title': 'Finish report', 'description': 'Complete the quarterly report', 'status': 'pending', 'due_date': '2025-10-20'},
  2: {'id': '2', 'title': 'Team meeting', 'description': '', 'status': 'done', 'due_date': '2025-10-18'},
  3: {'id': '3', 'title': 'Update website', 'description': 'Add new product info', 'status': 'pending', 'due_date': ''},
  4: {'id': '4', 'title': 'Client follow-up', 'description': 'Call client about feedback', 'status': 'done', 'due_date': '2025-10-19'},
  5: {'id': '5', 'title': 'Plan workshop', 'description': '', 'status': 'pending', 'due_date': '2025-10-25'},
  6: {'id': '6', 'title': 'Code review', 'description': 'Review PR #42', 'status': 'pending', 'due_date': ''},
  7: {'id': '7', 'title': 'Write blog post', 'description': 'Introduction to FastAPI', 'status': 'done', 'due_date': '2025-10-28'},
  8: {'id': '8', 'title': 'Deploy app', 'description': 'Deploy the latest version to production', 'status': 'pending', 'due_date': '2025-10-30'}
}
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        shutil.copy(test_file_path, tmp.name)
        tmp_path = Path(tmp.name)
    
    try:
        overwrite_csv(tmp_path, expected)
        dict_csv = {}
        with open(tmp_path ,newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                dict_csv[int(row["id"])] = row
            assert dict_csv == expected
    finally:
        tmp_path.unlink()