from langchain_core.documents import Document
from rag.knowledge_base import knowledge_base
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def build_documents():
    docs=[]

    for stage, content in knowledge_base.items():
        for section in ["goal","guidance","reflective_pitfalls"]:
            for text in content.get(section, []):
                docs.append(
                    Document(
                        page_content=text,
                        metadata={"stage": stage}
                    )
                )
    return docs

if __name__== "__main__":
    documents = build_documents()
    print(f"Total documents created: {len(documents)}")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Building FAISS vectorstore...")
    vectorstore = FAISS.from_documents(documents, embeddings)

    vectorstore.save_local("rag/vectorstore")

    print("Vectorstore saved successfully.")