from concurrent.futures import ThreadPoolExecutor

from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import get_embedding, get_embeddings, hf
from app.pinecone_db import index


generation_model = "openai/gpt-oss-120b:fastest"

ytt_api = YouTubeTranscriptApi()


def get_transcript(video_id):
    try:
        transcript = ytt_api.fetch(
            video_id,
            languages=["en"]
        )

        text = " ".join(
            snippet.text
            for snippet in transcript
        )

        return text

    except Exception as e:
        print("Transcript error:", e)
        return None


def split_transcript(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    return splitter.split_text(text)


def video_exists(video_id):
    result = index.query(
        vector=[1.0] + [0.0] * 767,
        top_k=1,
        filter={
            "video_id": video_id
        },
        include_metadata=False
    )

    return len(result["matches"]) > 0


def create_embedding(item):
    index_number, chunk = item

    try:
        vector = get_embedding(chunk)
        return index_number, chunk, vector

    except Exception as e:
        print(f"Embedding failed for chunk {index_number}: {e}")
        return None


def index_video(video_id, chunks):
    vectors = []

    batch_size = 20

    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i + batch_size]

        embeddings = get_embeddings(batch_chunks)

        for j, (chunk, vector) in enumerate(
            zip(batch_chunks, embeddings)
        ):
            chunk_index = i + j

            vectors.append({
                "id": f"{video_id}-{chunk_index}",
                "values": vector,
                "metadata": {
                    "video_id": video_id,
                    "chunk_id": chunk_index,
                    "text": chunk
                }
            })

        print(
            f"Embedded {min(i + batch_size, len(chunks))}/{len(chunks)}"
        )

    for i in range(0, len(vectors), 100):
        batch = vectors[i:i + 100]

        index.upsert(vectors=batch)

        print(
            f"Uploaded {min(i + 100, len(vectors))}/{len(vectors)}"
        )

    return len(vectors)


def retrieve_chunks(video_id, question, top_k=5):
    query_vector = get_embedding(question)

    result = index.query(
        vector=query_vector,
        top_k=top_k,
        filter={
            "video_id": video_id
        },
        include_metadata=True
    )

    return [
        match["metadata"]["text"]
        for match in result["matches"]
    ]


def generate_answer(question, context):
    prompt = f"""
Answer the question using only the provided context.

Context:
{context}

Question:
{question}

If the answer is not present in the context, say:
"I couldn't find the answer in the video."
"""

    response = hf.chat.completions.create(
        model=generation_model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=512,
        temperature=0.2
    )

    return response.choices[0].message.content


def ask_question(video_id, question):
    chunks = retrieve_chunks(
        video_id,
        question
    )

    if not chunks:
        return "I couldn't find relevant information in the video."

    context = "\n\n".join(chunks)

    return generate_answer(
        question,
        context
    )