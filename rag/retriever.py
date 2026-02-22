from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from rag.knowledge_base import knowledge_base

# Flatten knowledge per stage
def get_stage_documents(stage):
    kb = knowledge_base.get(stage, {})
    docs = []

    for section in ["goal", "guidance", "reflective_pitfalls"]:
        docs.extend(kb.get(section, []))

    return docs


def retrieve(stage, query, k=2):
    documents = get_stage_documents(stage)

    # Gabungkan query ke dalam corpus
    corpus = documents + [query]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Query adalah elemen terakhir
    query_vector = tfidf_matrix[-1]
    doc_vectors = tfidf_matrix[:-1]

    similarities = cosine_similarity(query_vector, doc_vectors)[0]

    # Ambil index top-k
    top_indices = similarities.argsort()[-k:][::-1]

    retrieved = [documents[i] for i in top_indices]

    return "\n".join(retrieved)