import os
from pymilvus import connections, utility
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Milvus
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from app.configs.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    FILEPATH,
    MILVUS_URI,
    COLLECTION_NAME,
)
from app.configs.logger.logging import logger

def initialize_vectorstore():
    logger.info("Initializing Milvus Vector Store...")
    
    # Milvus bağlantısı
    logger.info("Connecting to Milvus server...")
    connections.connect(alias="default", host="localhost", port="19530")

   # Embeddings
    embeddings = AzureOpenAIEmbeddings(  
    model="text-embedding-ada-002",            # Model adı
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,  # Doğru parametre kullanılıyor
    openai_api_version=AZURE_OPENAI_API_VERSION
    )

    # PDF kontrolü
    if not os.path.exists(FILEPATH):
        logger.error(f"PDF file not found: {FILEPATH}")
        raise FileNotFoundError(f"PDF file not found: {FILEPATH}")

    logger.info("Loading PDF...")
    loader = PyPDFLoader(FILEPATH)
    documents = loader.load()
    logger.info(f"Loaded {len(documents)} pages from PDF.")

    # Metin parçalama (chunk)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, 
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len
    )
    docs = text_splitter.split_documents(documents)

    logger.info(f"Split documents into {len(docs)} chunks.")
    logger.info(f"Creating/updating Milvus collection: {COLLECTION_NAME}")
    vectorstore = Milvus.from_documents(
        docs,
        embeddings,
        connection_args={"uri": MILVUS_URI},
        collection_name=COLLECTION_NAME
    )
    logger.info("Milvus Vector Store initialization complete.")
    return vectorstore
