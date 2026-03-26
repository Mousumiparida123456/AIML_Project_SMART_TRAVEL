import datetime
import json
import os
from pathlib import Path

import jwt
from werkzeug.security import check_password_hash, generate_password_hash


USERS_FILE = Path(__file__).resolve().with_name("users.json")
SECRET_KEY = os.environ.get("SMART_TRAVEL_SECRET_KEY", "dev-only-change-me")


def _load_users():
    if not USERS_FILE.exists():
        return {}
    try:
        return json.loads(USERS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _save_users(users):
    USERS_FILE.write_text(json.dumps(users, indent=2, sort_keys=True), encoding="utf-8")


def _normalize_token(auth_header_value):
    if not auth_header_value:
        return None
    value = auth_header_value.strip()
    if value.lower().startswith("bearer "):
        return value.split(" ", 1)[1].strip() or None
    return value


# ---------------- REGISTER ---------------- #
def register_user(username, password):
    if not username or not password:
        return False

    username = username.strip()
    if not username:
        return False

    users = _load_users()
    if username in users:
        return False

    users[username] = generate_password_hash(password)
    _save_users(users)
    return True


# ---------------- LOGIN ---------------- #
def login_user(username, password):
    if not username or not password:
        return None

    users = _load_users()
    stored_hash = users.get(username)
    if not stored_hash or not check_password_hash(stored_hash, password):
        return None

    token = jwt.encode(
        {"user": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
        SECRET_KEY,
        algorithm="HS256",
    )

    return token


# ---------------- VERIFY TOKEN ---------------- #
def verify_token(auth_header_value):
    token = _normalize_token(auth_header_value)
    if not token:
        return None

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return data.get("user")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
