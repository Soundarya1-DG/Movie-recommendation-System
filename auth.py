import json
import os

USER_FILE = "users.json"

# Load users from file
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

# Save users to file
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# Add new user
def add_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = password
    save_users(users)
    return True

# Validate user credentials
def validate_login(username, password):
    users = load_users()
    return username in users and users[username] == password
