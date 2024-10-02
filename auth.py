import os
import json
import streamlit as st

AUTH_FILE = "auth.json"


def load_auth_data():
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "r") as f:
            return json.load(f)
    return {}


def save_auth_data(data):
    with open(AUTH_FILE, "w") as f:
        json.dump(data, f)


def login(username, password):
    auth_data = load_auth_data()
    if username in auth_data and auth_data[username] == password:
        return True
    return False


def check_authentication():
    return st.session_state.get('authenticated', False)


def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
