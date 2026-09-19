from app.config import get_embedding
from app.pinecone_db import index

text = "RAG retrieves relevant information from documents."

vector = get_embedding(text)

index.upsert(
    vectors=[
        {
            "id": "test-1",
            "values": vector,
            "metadata": {
                "text": text
            }
        }
    ]
)

print("Vector uploaded successfully")