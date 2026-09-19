from app.config import get_embedding

embedding = get_embedding("RAG retrieves relevant information.")

print(type(embedding))
print(len(embedding))