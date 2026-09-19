from app.rag import ask_question

video_id = "o126p1QN_RI"

question = "What is the main topic discussed in this video?"

answer = ask_question(
    video_id,
    question
)

print("\nAnswer:\n")
print(answer)