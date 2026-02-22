print("START TEST")

from rag.retriever import retrieve

query = "aku takut gagal dan jadi menunda"

print("Running retrieval...")

result = retrieve(stage="reasoning", query=query, k=2)

print("DONE RETRIEVE")

print("\nRetrieved Knowledge:\n")
print(result)