from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pydantic import BaseModel
from typing import List
import os
from pathlib import Path
import shutil
import datetime
from passlib.hash import bcrypt
import jwt
from fastapi import Depends, Header
from jwt import PyJWTError

# Simple JWT settings (replace secret in production)
SECRET_KEY = "changeme_quick_dev_only"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "api_data.db"
POSTCARDS_DIR = BASE_DIR / "postcards"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS wishlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        UNIQUE(user_id, name)
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS postcards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        filename TEXT,
        title TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()
    POSTCARDS_DIR.mkdir(parents=True, exist_ok=True)


class Item(BaseModel):
    name: str


class UserIn(BaseModel):
    username: str
    password: str


def create_access_token(*, data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except PyJWTError:
        return None


def get_user_id_by_username(username: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def get_current_username(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid auth header")
    token = parts[1]
    username = decode_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username


def get_optional_username(authorization: str = Header(None)):
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    token = parts[1]
    username = decode_token(token)
    return username


app = FastAPI(title="OffMap API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/wishlist", response_model=List[str])
def get_wishlist(username: str = Depends(get_current_username)):
    user_id = get_user_id_by_username(username)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM wishlist WHERE user_id = ? ORDER BY name", (user_id,))
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows


@app.post("/wishlist", status_code=201)
def add_wishlist(item: Item, username: str = Depends(get_current_username)):
    user_id = get_user_id_by_username(username)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO wishlist(user_id, name) VALUES (?, ?)", (user_id, item.name))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Item already exists")
    conn.close()
    return {"added": item.name}


@app.delete("/wishlist/{name}")
def delete_wishlist(name: str, username: str = Depends(get_current_username)):
    user_id = get_user_id_by_username(username)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM wishlist WHERE user_id = ? AND name = ?", (user_id, name))
    conn.commit()
    conn.close()
    return {"deleted": name}


@app.delete("/wishlist/clear")
def clear_wishlist(username: str = Depends(get_current_username)):
    user_id = get_user_id_by_username(username)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM wishlist WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return {"cleared": True}


@app.post("/postcards")
async def upload_postcard(file: UploadFile = File(...), title: str = Form(...), username: str = Depends(get_optional_username)):
    # Save uploaded file
    filename = f"{int(datetime.datetime.utcnow().timestamp())}_{file.filename}"
    dest = POSTCARDS_DIR / filename
    with open(dest, "wb") as out:
        content = await file.read()
        out.write(content)

    # Save metadata (associate with user if provided)
    user_id = None
    if username:
        user_id = get_user_id_by_username(username)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO postcards(user_id, filename, title, created_at) VALUES (?, ?, ?, ?)", (user_id, filename, title, datetime.datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

    return {"url": f"/postcards/{filename}", "filename": filename}


@app.get("/postcards")
def list_postcards():
    files = []
    for p in sorted(POSTCARDS_DIR.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
        files.append({"filename": p.name, "url": f"/postcards/{p.name}"})
    return files


@app.get("/postcards/{filename}")
def get_postcard(filename: str):
    p = POSTCARDS_DIR / filename
    if not p.exists():
        raise HTTPException(status_code=404, detail="Not found")
    return FileResponse(p)


@app.post("/auth/register")
def register(user: UserIn):
    username = user.username
    password = user.password
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password required")
    pw_hash = bcrypt.hash(password)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users(username, password_hash) VALUES (?, ?)", (username, pw_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="username exists")
    conn.close()
    return {"created": username}


@app.post("/auth/login")
def login(user: UserIn):
    username = user.username
    password = user.password
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=400, detail="invalid credentials")
    pw_hash = row[0]
    if not bcrypt.verify(password, pw_hash):
        raise HTTPException(status_code=400, detail="invalid credentials")
    token = create_access_token(data={"sub": username})
    return {"access_token": token, "token_type": "bearer"}
