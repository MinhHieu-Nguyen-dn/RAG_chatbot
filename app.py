import streamlit as st
from auth import login, check_authentication, logout
from file_management import initialize_folders, upload_files, list_user_files, delete_file, save_api_key
from rag_interface import encode_documents, chat_interface

# Initialize necessary folders
initialize_folders()

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
st.sidebar.title("Navigation")

if not st.session_state.authenticated:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if login(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.rerun()
        else:
            st.sidebar.error("Invalid credentials")
else:
    st.sidebar.write(f"Logged in as: {st.session_state.username}")
    if st.sidebar.button("Logout"):
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
                st.success("API Key saved successfully!")
            else:
                st.error("Error saving API Key.")

        # Encode documents
        if st.button("Encode Documents"):
            with st.spinner("Encoding documents..."):
                encode_documents(st.session_state.username)
            st.success("Documents encoded successfully!")

    elif page == "Ask my Documents":
        st.title("Ask my Documents")
        chat_interface(st.session_state.username)

else:
    st.title("Welcome to DocsChat")
    st.subheader("Ask your documents about your documents!")
    st.write("Please login to use the application.")
