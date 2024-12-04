import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from datetime import datetime

#updates vector db with docs
def update_vector_store(vector_store, new_files, chunk_size=1000, chunk_overlap=100):
    #split/load the docs
    new_documents = []
    for file_path in new_files:
        if os.path.exists(file_path):
            loader = PyPDFLoader(file_path)
            new_documents.extend(loader.load())
        else:
            print(f"Can't find it....: {file_path}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    new_chunks = splitter.split_documents(new_documents)

    #add chunks to vector storage
    embeddings = OpenAIEmbeddings()
    vector_store.add_documents(new_chunks, embeddings)
    print(f"Added {len(new_chunks)} new chunks to the vector store!!!!")
    
    return vector_store


#log queries (helps debug stuff)
def log_query_response(query, response, log_file="query_logs.txt"):
    with open(log_file, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] Query:\n{query}\n")
        f.write(f"Response:\n{response}\n")
        f.write("="*50 + "\n")
    print(f"Logged query and response to {log_file}")


#initialize the vector storage
def initialize_vector_store(file_paths, chunk_size=1000, chunk_overlap=100):
    documents = []
    for path in file_paths:
        loader = PyPDFLoader(path)
        documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(documents)
    
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    print(f"Initialized vector store with {len(chunks)} chunks from {len(file_paths)} files!!!!!")
    return vector_store
