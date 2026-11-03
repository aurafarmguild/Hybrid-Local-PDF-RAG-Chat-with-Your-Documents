from backend.rag_engine import process_pdf

pdf_path = "data/uploads/Everything-to-know-about-RAG.pdf"

chunks = process_pdf(pdf_path)

print("Total chunks:", len(chunks))

print("\nFirst chunk:")
print(chunks[0])

print("\nLast chunk:")
print(chunks[-1])
