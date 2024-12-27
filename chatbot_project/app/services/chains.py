from app.configs.logger.logging import logger
from pymilvus import utility
import os
from pathlib import Path
from jinja2 import FileSystemLoader, Environment
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI
from app.services.vectorstore import initialize_vectorstore
from app.configs.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
)

# Şablon dosyalarını yükle
SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"
env = Environment(loader=FileSystemLoader(str(SCHEMAS_DIR)))

if not SCHEMAS_DIR.exists():
    raise FileNotFoundError(f"Schemas directory not found at: {SCHEMAS_DIR}")

contextualize_q_template = env.get_template('contextualize_q_prompt.jinja2')
qa_system_template = env.get_template('qa_system_prompt.jinja2')

# Milvus veritabanını başlat
try:
    db = initialize_vectorstore()
except Exception as e:
    logger.error("Failed to initialize Milvus Vector Store: %s", e)
    raise e

collections = utility.list_collections()
print("Collections in Milvus:", collections)

# Azure Chat OpenAI modeli
llm = AzureChatOpenAI(
    model="gpt-4o",
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    openai_api_version=AZURE_OPENAI_API_VERSION
)

# Şablonlar
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_template.render()),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_template.render(context="{context}")),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# Sabit Retriever Fonksiyonu
def get_rag_chain(chat_history, query):
    """
    similarity_score_threshold kullanan sabit bir retriever oluşturur.
    """
    top_k = 5  # Sabit sonuç sayısı
    score_threshold = 0.6  # Sabit skor eşik değeri
    
    # Sabit retriever oluşturma
    static_retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k, "score_threshold": score_threshold}
    )
    
    # History aware retriever
    history_aware_retriever = create_history_aware_retriever(llm, static_retriever, contextualize_q_prompt)
    
    # RAG Chain
    return create_retrieval_chain(history_aware_retriever, question_answer_chain)
