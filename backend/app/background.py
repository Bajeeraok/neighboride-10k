import requests
import os

CHECKR_API_KEY = os.getenv("CHECKR_API_KEY")
BASE_URL = "https://api.checkr.com/v1"

def initiate_background_check(user_id: int, user_email: str):
    headers = {"Authorization": f"Bearer {CHECKR_API_KEY}"}
    data = {
        "candidate": {
            "email": user_email,
            "first_name": "Test", # From user model
            "last_name": "Driver"
        },
        "package": "driver" # Basic motor vehicle + criminal
    }
    response = requests.post(f"{BASE_URL}/background_checks", json=data, headers=headers)
    if response.status_code == 201:
        report_id = response.json()["id"]
        # Update user with report_id
        return report_id
    raise Exception("Checkr request failed")