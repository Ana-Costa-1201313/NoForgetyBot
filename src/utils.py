
from datetime import datetime
import json

def validate_date(date: str) -> bool:
    try:
        datetime.strptime(f"2000-{date}", "%Y-%m-%d")
        return True
    except ValueError:
        return False

def load_data(file: str):
    with open(file, 'r') as f:
        return json.load(f)

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)
