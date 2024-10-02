import os
import sqlite3
import bcrypt
import re
import streamlit as st

# Define the path for the database
DB_NAME = "users.sqlite"
DB_PATH = os.path.join("credentials", DB_NAME)


def init_db():
    # Ensure the directory exists
    os.makedirs("credentials", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
               (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()


def is_valid_username(username):
    # Username should be alphanumeric and between 3 and 20 characters
    return re.match(r'^[a-zA-Z0-9]{3,20}$', username) is not None


def register(username, password):
    if not is_valid_username(username):
        return False, "Invalid username. Use 3-20 alphanumeric characters."

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already taken"
    finally:
        conn.close()

    return True, "Registration successful! Please login to continue."


def login(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()

    if result is None:
        return False

    stored_password = result[0]
    return bcrypt.checkpw(password.encode('utf-8'), stored_password)


def check_authentication(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result is not None


def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
