import json
from datetime import datetime

def log_admin_action(admin_username, action_type, service_type, details):
    """
    Log admin actions to a JSON file.
    
    Args:
        admin_username (str): Username of the admin performing the action
        action_type (str): Type of action (add/remove/update)
        service_type (str): Type of service (flight/bus/train/hotel/car)
        details (dict): Additional details about the action
    """
    try:
        with open("data/admin_logs.json", "r", encoding="utf-8") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = {}
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "admin_username": admin_username,
        "action_type": action_type,
        "service_type": service_type,
        "details": details
    }
    
    if timestamp not in logs:
        logs[timestamp] = log_entry
    
    with open("data/admin_logs.json", "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

def get_admin_logs():
    """
    Retrieve all admin logs.
    
    Returns:
        dict: Dictionary containing all admin logs
    """
    try:
        with open("data/admin_logs.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {} 