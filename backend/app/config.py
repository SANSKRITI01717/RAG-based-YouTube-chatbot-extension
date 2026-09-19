import os

from huggingface_hub import InferenceClient
from pinecone import Pinecone

HF_TOKEN = os.getenv("HF_TOKEN")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

hf = InferenceClient(
    api_key=HF_TOKEN
)

pc = Pinecone(
    api_key=PINECONE_API_KEY
)

def get_embedding(text):
    embedding = hf.feature_extraction(text)

    if embedding.ndim == 2:
        embedding = embedding.mean(axis=0)

    return embedding.tolist()

def get_embeddings(texts):
    embeddings = hf.feature_extraction(texts)

    if embeddings.ndim == 3:
        embeddings = embeddings.mean(axis=1)

    return embeddings.tolist()