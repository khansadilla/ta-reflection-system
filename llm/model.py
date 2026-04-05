from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    frequency_penalty=0.6,
    request_timeout=20
)

llm_judge = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    request_timeout=20
)
