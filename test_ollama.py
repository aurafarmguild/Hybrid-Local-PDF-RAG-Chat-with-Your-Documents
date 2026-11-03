from backend.generator import generate_answer

context = """
RAG stands for Retrieval-Augmented Generation.
It combines information retrieval with text generation.
It allows an AI model to retrieve relevant external information
before generating an answer.
[Source: Everything-to-know-about-RAG.pdf, Page 1]
"""

question = "What does RAG stand for?"

answer = generate_answer(question, context)

print("\nQuestion:", question)
print("\nAnswer:", answer)