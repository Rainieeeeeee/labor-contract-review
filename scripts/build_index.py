import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os
from parse_laws import parse_law

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="labor_laws")

def build_index(file_path):
    chunks = parse_law(file_path)
    for chunk in chunks:
        response = client.embeddings.create(
            input = chunk["content"],
            model = "text-embedding-3-small"
        )
        vector = response.data[0].embedding

        collection.add(
            ids=[chunk["article_number"]],
            embeddings=[vector],
            documents=[chunk["content"]],
            metadatas=[{
                "law_name": chunk["law_name"],
                "article_number": chunk["article_number"],
                "effective_date": chunk["effective_date"]
            }]
        )

if __name__ == "__main__":
    build_index("data/laws/中华人民共和国劳动合同法_20121228.txt")
    print("索引构建完成")
