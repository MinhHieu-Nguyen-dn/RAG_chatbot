import os


def get_user_data_path(username):
    return os.path.join("data", username)


def get_user_index_path(username):
    return os.path.join("index", username)


def get_user_env_path(username):
    return os.path.join("env", f"{username}.env")


def initialize_folders():
    base_folders = ["data", "index", "env"]
    for folder in base_folders:
        os.makedirs(folder, exist_ok=True)


def upload_files(uploaded_files, username):
    user_data_path = get_user_data_path(username)
    os.makedirs(user_data_path, exist_ok=True)

    successful_uploads = 0
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            file_path = os.path.join(user_data_path, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            successful_uploads += 1

    return successful_uploads


def delete_file(filename, username):
  user_data_path = get_user_data_path(username)
  file_path = os.path.join(user_data_path, filename)
  if os.path.exists(file_path):
      os.remove(file_path)
      return True
  return False


def list_user_files(username):
    user_data_path = get_user_data_path(username)
    if not os.path.exists(user_data_path):
        return []
    return [f for f in os.listdir(user_data_path) if f.endswith('.pdf')]


def save_api_key(api_key, username):
    env_path = get_user_env_path(username)
    os.makedirs(os.path.dirname(env_path), exist_ok=True)
    with open(env_path, "w") as f:
        f.write(f"OPENAI_API_KEY=\"{api_key}\"")
    return True
