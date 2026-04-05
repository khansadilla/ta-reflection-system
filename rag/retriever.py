import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_FAISS_PATH = "rag/vectorstore"

# Global cache (biar ga load berulang)
_embeddings = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        print(">>> Loading embeddings model...")
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}  # biar stabil
        )
        print(">>> Embeddings loaded")
    return _embeddings

_vectorstore = None

def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        embeddings = get_embeddings()
        print(">>> Loading vectorstore...")
        _vectorstore = FAISS.load_local(
            DB_FAISS_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
        print(">>> Vectorstore loaded")
    return _vectorstore

def retrieve(stage, query, k=2):
    try:
        if not os.path.exists(DB_FAISS_PATH):
            print(f"Error: Folder {DB_FAISS_PATH} tidak ditemukan.")
            return ""

        embeddings = get_embeddings()

        vectorstore = get_vectorstore()

        results = vectorstore.similarity_search(
            query,
            k=k,
            filter={"stage": stage}
        )

        if not results:
            return "Tidak ada pedoman spesifik ditemukan untuk tahap ini."

        return "\n".join([doc.page_content for doc in results])

    except Exception as e:
        print(f"Terjadi kesalahan saat retrieval: {e}")
        return ""