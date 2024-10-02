# DocsChat

DocsChat is a Streamlit-based RAG (Retrieval-Augmented Generation) chatbot application that allows users to interact with their documents through a conversational interface.

*The author is learning to implement "all" RAG techniques while creating this project. The project is still in development.*

## Features

- User authentication (registration and login);
- File management (upload, list, and delete PDF documents);
- Document encoding (embeddings) for efficient retrieval;
- Conversational interface to ask questions (one-by-one) about uploaded documents.

## RAG Technique (to be updated)
- v1 (October 2, 2024): Simple RAG with FAISS (branch: `simple-rag`)

## Quick Start (latest version)
Access: https://datum-docs-chat.streamlit.app/

## Install and Run on your Machine

1. Clone the repository:
   ```
   git clone https://github.com/MinhHieu-Nguyen-dn/RAG_chatbot
   cd RAG_chatbot
   ```

2. Create a virtual environment and activate it:
   ```
   conda create -n RAG python=3.12
   conda activate RAG
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Register a new account or log in if you already have one.

4. Upload your PDF documents in the "Files & Credentials" section.

5. Enter your OpenAI API key in the designated field.

6. Click on "Encode Documents" to prepare your documents for querying.

7. Navigate to the "Ask my Documents" section to start chatting with your documents.


## Security Note

Basic standard.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.