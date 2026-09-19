from app.rag import (
    get_transcript,
    split_transcript,
    index_video,
    video_exists
)

video_id = "o126p1QN_RI"

if video_exists(video_id):
    print("Video already indexed")
    exit()

text = get_transcript(video_id)

if not text:
    print("Transcript not found")
    exit()

chunks = split_transcript(text)

print("Transcript length:", len(text))
print("Chunks:", len(chunks))

count = index_video(
    video_id,
    chunks
)

print("Vectors uploaded:", count)