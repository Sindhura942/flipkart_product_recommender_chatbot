import os
from dotenv import load_dotenv

load_dotenv()
class Config:
  
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")
    RAG_MODEL = "gpt-4"
    EMBEDDING_MODEL = "text-embedding-3-small"
