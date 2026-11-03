
from backend.rag_engine import process_pdf
from backend.retrieval import HybridRetriever
from backend.generator import answer_question


# 1. Load and process the PDF
pdf_path = "data/uploads/Everything-to-know-about-RAG.pdf"

chunks = process_pdf(pdf_path)

print("PDF processed:", len(chunks), "chunks")


# 2. Initialize hybrid retrieval
retriever = HybridRetriever(chunks)


# 3. Ask a question
question = "What is semantic search?"

print("\nQuestion:", question)


# 4. Retrieve relevant chunks
results = retriever.retrieve(
    query=question,
    candidate_k=20,
    final_k=5
)

print("\n========== RETRIEVAL SCORES ==========")

for i, chunk in enumerate(results, start=1):
    print(f"\nResult {i}")
    print(f"Page: {chunk['page']}")
    print(f"Score: {chunk['rerank_score']:.4f}")
    print(f"Content:\n{chunk['text'][:400]}")

print("\n========== ALL RETRIEVED CHUNKS ==========")

for i, chunk in enumerate(results, start=1):
    print(f"\nResult {i}")
    print(f"Page: {chunk['page']}")
    print(f"Score: {chunk['rerank_score']:.4f}")
    print(f"Content:\n{chunk['text']}")

print("\n======================================")

# 5. Generate an answer using Ollama
print("\nGenerating answer...")

answer = answer_question(question, results)


# 6. Display final answer
print("\n========== RAG ANSWER ==========\n")

print(answer)

print("\n================================")
