import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="labor_laws")

def retrieve(clause_text, n_results=3):
    response = client.embeddings.create(
            input = clause_text,
            model = "text-embedding-3-small"
        )
    vector = response.data[0].embedding 

    result = collection.query(
        query_embeddings=[vector],
        n_results=n_results
    )
    return result