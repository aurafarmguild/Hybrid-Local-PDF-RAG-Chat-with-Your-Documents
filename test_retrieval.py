from backend.rag_engine import process_pdf
from backend.retrieval import HybridRetriever


# 1. Process the PDF
pdf_path = "data/uploads/Everything-to-know-about-RAG.pdf"

chunks = process_pdf(pdf_path)

print("Total chunks:", len(chunks))


# 2. Build the retrieval system
retriever = HybridRetriever(chunks)


# 3. Ask a test question
question = "What is Retrieval-Augmented Generation?"

results = retriever.retrieve(
    query=question,
    candidate_k=20,
    final_k=5
)


# 4. Display retrieved results
print("\nQuestion:", question)
print("\nTop retrieved chunks:\n")

for i, result in enumerate(results, start=1):

    print(f"\nResult {i}")
    print("Source:", result["source"])
    print("Page:", result["page"])
    print("RRF Score:", round(result["rrf_score"], 5))
    print("Rerank Score:", round(result["rerank_score"], 4))
    print("Text:", result["text"][:400])
    print("-" * 60)