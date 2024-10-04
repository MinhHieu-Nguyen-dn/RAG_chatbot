import streamlit as st
from auth import init_db, register, login, logout
from file_management import initialize_folders, upload_files, list_user_files, delete_file, save_api_key
from rag_interface import encode_documents, chat_interface
import time

# Initialize necessary folders and database
initialize_folders()
init_db()

# Set page config
st.set_page_config(page_title="DocsChat", layout="wide")
# Set default page name
page = "Files & Credentials"

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Sidebar
st.sidebar.title("DocsChat Navigator")

if not st.session_state.authenticated:
    auth_option = st.sidebar.radio("Please login to continue:", ["Login", "Don't have an account? Register"])

    if auth_option == "Login":
        username = st.sidebar.text_input("Username", value='')
        password = st.sidebar.text_input("Password", type="password", value='')
        if st.sidebar.button("Login"):
            if login(username, password):
                login_time = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"--- {login_time} --- USER LOGIN: User {username} logged in.")
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()
            else:
                st.sidebar.error("Invalid credentials")
    else:
        username = st.sidebar.text_input("Register Username", value='')
        password = st.sidebar.text_input("Register Password", type="password", value='')
        confirm_password = st.sidebar.text_input("Confirm Register Password", type="password", value='')
        if st.sidebar.button("Register"):
            if password != confirm_password:
                st.sidebar.error("Passwords do not match")
            else:
                success, message = register(username, password)
                if success:
                    signup_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    print(f"--- {signup_time} --- USER SIGNUP: User {username} signed up.")
                    st.sidebar.success(message)
                    st.session_state.authenticated = False
                    st.session_state.username = None
                else:
                    st.sidebar.error(message)
else:
    st.sidebar.write(f"Logged in as: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        logout_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"--- {logout_time} --- USER SIGNUP: User {st.session_state.username} logged out.")
        logout()
        st.rerun()

    # Navigation
    page = st.sidebar.radio("Go to", ["Files & Credentials", "Ask my Documents"])

# Main content
if st.session_state.authenticated:
    if page == "Files & Credentials":
        st.title("Files & Credentials")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Upload Files")
            uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
            if uploaded_files:
                if st.button("Upload Selected Files"):
                    successful_uploads = upload_files(uploaded_files, st.session_state.username)
                    if successful_uploads:
                        st.success(f"Successfully uploaded {successful_uploads} file(s)!")
                        uploads_time = time.strftime("%Y-%m-%d %H:%M:%S")
                        print(f"--- {uploads_time} --- FILES UPLOAD: User {st.session_state.username} uploaded {successful_uploads} file(s).")
                    else:
                        st.error("Error uploading files.")

        with col2:
            st.subheader("Your Files")
            user_files = list_user_files(st.session_state.username)
            if user_files:
                for file in user_files:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(file)
                    with col2:
                        if st.button("Delete", key=f"delete_{file}"):
                            if delete_file(file, st.session_state.username):
                                st.success(f"Deleted {file}")
                                st.rerun()
                            else:
                                st.error(f"Error deleting {file}")
            else:
                st.info("No files uploaded yet.")

        # OpenAI API Key input
        st.subheader("OpenAI API Key")
        api_key = st.text_input("Enter your OpenAI API Key", type="password")
        if st.button("Save API Key"):
            if save_api_key(api_key, st.session_state.username):
                save_api_key_time = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"--- {save_api_key_time} --- API KEY SAVED: User {st.session_state.username} saved an API Key.")
                st.success("API Key saved successfully!")
            else:
                st.error("Error saving API Key.")

        # Encode documents
        if st.button("Encode Documents"):
            with st.spinner("Encoding documents..."):
                encode_documents(st.session_state.username)
            st.success("Documents encoded successfully!")
            encoded_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"--- {encoded_time} --- ENCODE DOCUMENTS: User {st.session_state.username} encoded documents successfully.")

    elif page == "Ask my Documents":
        st.title("Ask my Documents")
        chat_interface(st.session_state.username)

else:
    st.title("Welcome to DocsChat")
    st.subheader("Ask your documents about your documents!")
    st.write("Please login to use the application.")
