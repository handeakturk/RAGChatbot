import os
from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_MODEL_NAME = os.getenv("AZURE_MODEL_NAME")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

# Yapılandırma ayarları
# Retriever yapılandırmaları
TOP_K = 5
SCORE_THRESHOLD = 0.6
SEARCH_TYPE = "similarity_score_threshold"


CHUNK_SIZE = 1500
CHUNK_OVERLAP = 300
FILEPATH = os.path.join(os.path.dirname(__file__), "doc", "banka.pdf")
MILVUS_URI = "http://localhost:19530"
COLLECTION_NAME = "banka_collection"


