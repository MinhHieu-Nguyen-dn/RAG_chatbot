"""
Implementation of Simple RAG.
Best used for learning with *centralized* functions and modules of code with explanation comments for easy access and modification.

# TO-DO: Add more details about dependencies and usage.

"""

import os
import sys
import time
# from dotenv import load_dotenv

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Add the parent directory (the RAG_TECHNIQUES directory) to the path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

# Load environment variables from a .env file(for OpenAI API Key)
# load_dotenv()
# os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')


class SimpleRAG:
    """
    Simple RAG process for:
    - Documents pre-processing (chunking)
    - Documents indexing (vector embeddings store) with FAISS
    - Context retrieval for queries
    """

    def __init__(self):
        """
        Initializes the SimpleRAG object.
        """

        print("\n--- Initializing SimpleRAG Object ---")
        self.time_records = {}

    def encode_documents(self, data_path, index_path, model_embedding, chunk_size=1000, chunk_overlap=200):
        """
        Encode documents into vector embeddings after chunking (by file).
        Encoding with model_embedding.

        Args:
            data_path (str): Path to the directory containing the documents (PDF) to encode.
            index_path (str): Path to save/load the index files.
            model_embedding: Model instance for the embeddings (e.g., OpenAI).
            chunk_size (int): Size of each text chunk (default: 1000).
            chunk_overlap (int): Overlap between consecutive chunks (default: 200).

        Returns: document embeddings index in index_path.
        """

        def replace_tab_with_space(list_of_chunks):
            """
            Replace tabs ('\t') with spaces (' ') for each chunk of content in the list.

            Args:
                list_of_chunks (list): List of document chunks.

            Returns:
                Modified list of document chunks with tabs replaced by spaces.
            """

            for chunk in list_of_chunks:
                chunk.page_content = chunk.page_content.replace('\t', ' ')
            return list_of_chunks

        print(f"\n{time.strftime("%Y-%m-%d %H:%M:%S")} --- SimpleRAG - Process Starts: Encoding documents---")

        start_time = time.time()
        # Documents chunking
        print("\n--- Chunking documents ---")

        all_chunks = []

        for filename in os.listdir(data_path):
            doc_path = os.path.join(data_path, filename)

            # Load PDF
            loader = PyPDFLoader(doc_path)
            doc = loader.load()

            # Split document into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
            )
            chunks = text_splitter.split_documents(doc)
            cleaned_text_chunks = replace_tab_with_space(chunks)
            all_chunks.extend(cleaned_text_chunks)

        chunking_time = time.time() - start_time
        self.time_records['Chunking'] = chunking_time

        # Encode the documents into a vector store using model_embedding
        print(f"\n{time.strftime("%Y-%m-%d %H:%M:%S")} --- Creating vectorstore for document embeddings index ---")
        vectorstore = FAISS.from_documents(all_chunks, model_embedding)

        embedding_time = time.time() - start_time
        self.time_records['Embedding'] = embedding_time

        # Save the encoded documents index to index_path
        print(f"\n{time.strftime("%Y-%m-%d %H:%M:%S")} --- Saving the encoded documents index ---")
        print(f'Index path: {index_path}')
        print(f'Total index count: {vectorstore.index.ntotal}')
        vectorstore.save_local(index_path)

        print(f"\n{time.strftime("%Y-%m-%d %H:%M:%S")} Process Completed! Chunking Time: {chunking_time:.2f} seconds; Embedding Time: {embedding_time:.2f} seconds.")

    def retrieve_context(self, index_path, model_embedding, query, k_retrieved=3):
        """
        Retrieve context for the given query.

        Args:
            index_path (str): Path to save/load the index files.
            model_embedding: Model instance for the embeddings (e.g., OpenAI).
            query (str): User's question or query to retrieve context for.
            k_retrieved (int): Number of chunks to retrieve for each query (default: 3).

        Returns:
            Retrieval context and time.
        """
        print(f"\n{time.strftime("%Y-%m-%d %H:%M:%S")} --- SimpleRAG - Process Starts: Retrieving Contexts---")

        # Create a retriever from the vector store index
        print('\n--- Loading index retriever ---')
        embeddings_index = FAISS.load_local(folder_path=index_path, embeddings=model_embedding,
                                            allow_dangerous_deserialization=True)
        chunks_query_retriever = embeddings_index.as_retriever(search_kwargs={"k": k_retrieved})

        print(f"\n--- Retrieving context for query: \"{query}\"---")
        start_time = time.time()

        # Retrieve context for the query from the encoded documents index
        docs = chunks_query_retriever.get_relevant_documents(query)

        # Concatenate document content
        contexts = [doc.page_content for doc in docs]

        retrieval_time = time.time() - start_time
        self.time_records['Retrieval'] = retrieval_time

        # Return the retrieved context and time
        print(f"\n{time.strftime("%Y-%m-%d %H:%M:%S")}--- Context retrieval completed ---")
        print(f"Retrieval Time: {retrieval_time:.2f} seconds")

        # Display the retrieved context
        for index, context in enumerate(contexts):
            print(f'Context {index + 1}:')
            print(context)
            print('\n')

        return contexts

    def evaluate_rag(self):
        """
        Evaluate the Simple RAG retriever.
        """
        return None
        # TODO: Prepare ground-truth Question-Answers for this evaluation
        # print("\n--- Evaluating Simple RAG Retriever ---")
        # evaluate_rag(self.chunks_query_retriever)


def main():
    # Create data and index directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('index', exist_ok=True)

    # Path to get data (knowledge/contexts) files
    DATA_PATH = os.path.join(os.getcwd(), 'data')
    print(f'Data path = {DATA_PATH}')

    # Path to save/load index files
    INDEX_PATH = os.path.join(os.getcwd(), 'index')
    print(f'Index path = {INDEX_PATH}')

    model_embeddings = OpenAIEmbeddings()
    chunk_size = 3000
    chunk_overlap = 200

    rag_instance = SimpleRAG()
    rag_instance.encode_documents(DATA_PATH, INDEX_PATH, model_embeddings, chunk_size, chunk_overlap)

    # Query for context retrieval
    query = input("Enter your query: ")
    rag_instance.retrieve_context(INDEX_PATH, model_embeddings, query)


if __name__ == '__main__':
    main()
