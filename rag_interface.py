import streamlit as st
from dotenv import load_dotenv
from file_management import get_user_data_path, get_user_index_path, get_user_env_path
from rag import SimpleRAG
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import time


def load_user_env(username):
    env_path = get_user_env_path(username)
    load_dotenv(env_path)


def encode_documents(username):
    load_user_env(username)
    data_path = get_user_data_path(username)
    index_path = get_user_index_path(username)
    model_embeddings = OpenAIEmbeddings()
    chunk_size = 3000
    chunk_overlap = 200

    rag = SimpleRAG()
    rag.encode_documents(data_path, index_path, model_embeddings, chunk_size, chunk_overlap)


def chat_interface(username):
    load_user_env(username)
    index_path = get_user_index_path(username)
    model_embeddings = OpenAIEmbeddings()
    k_documents = 3

    rag_instance = SimpleRAG()

    # st.subheader("Chat with your documents")
    user_input = st.text_input("Enter your question:")

    if user_input:
        with st.spinner("Retrieving context and generating response..."):
            query_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"--- {query_time} --- QUESTION: User {st.session_state.username} asked: \"{user_input}\"")

            contexts = rag_instance.retrieve_context(index_path, model_embeddings, user_input, k_documents)

            # Use ChatOpenAI for response generation
            chat_model = ChatOpenAI(temperature=0, model_name="gpt-4o", max_tokens=4000)
            response = chat_model.predict(f"Context: {contexts}\n\nQuestion: {user_input}\n\nAnswer:")

            st.write("Response:")
            st.write(response)
            response_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"--- {response_time} --- RESPONSE: Responded to user {st.session_state.username}: \"{response}\"")
