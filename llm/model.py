from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

'''
llm = ChatOpenAI(
    model="gpt-4o-mini", 
    temperature=0.7
)
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    frequency_penalty=0.6,
    request_timeout=20
)'''

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    temperature=0.7
)


llm_judge = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    request_timeout=20
)
