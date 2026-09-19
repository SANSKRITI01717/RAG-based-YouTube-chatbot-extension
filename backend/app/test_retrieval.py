from app.config import get_embedding
from app.pinecone_db import index

video_id = "o126p1QN_RI"

question = "What is the main topic discussed in this video?"

query_vector = get_embedding(question)

result = index.query(
    vector=query_vector,
    top_k=5,
    filter={
        "video_id": video_id
    },
    include_metadata=True
)

print("Matches:", len(result["matches"]))

for match in result["matches"]:
    print("\nScore:", match["score"])
    print("Video:", match["metadata"].get("video_id"))
    print("Chunk:", match["metadata"].get("chunk_id"))
    print("Text:", match["metadata"].get("text")[:300])