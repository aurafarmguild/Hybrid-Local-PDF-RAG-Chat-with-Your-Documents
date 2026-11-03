# Hybrid-Local-PDF-RAG-Chat-with-Your-Documents

**Overview**

Developed an end-to-end Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask natural-language questions about their contents.

Implemented a hybrid retrieval pipeline combining BM25 keyword search and semantic vector search, followed by Reciprocal Rank Fusion and cross-encoder reranking to improve retrieval relevance.

Integrated a locally running Qwen 2.5 model through Ollama to generate context-grounded answers, with evidence checking, answer verification, and source-page citations.

Built a FastAPI backend to expose document upload and question-answering endpoints, alongside a Streamlit interface for document interaction.

**Technologies**: Python, FastAPI, Streamlit, Ollama, Qwen 2.5, Sentence Transformers, BM25, Reciprocal Rank Fusion (RRF), Cross-Encoder Reranking, PyPDF.

**Key Features**
- Dynamic PDF uploading and processing.
- Text extraction and recursive chunking.
- Hybrid keyword and semantic retrieval.
- Reciprocal Rank Fusion and cross-encoder reranking.
- Locally hosted LLM inference using Ollama.
- Evidence-based answer generation and source citations.
- REST API integration using FastAPI.
- Interactive document-question-answering interface using Streamlit.

**Engineering Highlights**

Designed a modular Python architecture separating PDF processing, retrieval, generation, and API responsibilities. Tested the system using multiple PDFs with different content and document sizes.

The application allows users to:
- Upload their own PDF documents.
- Extract and divide PDF content into smaller chunks.
- Search documents using keyword and semantic retrieval.
- Combine search results using Reciprocal Rank Fusion (RRF).
- Rerank results using a cross-encoder.
- Generate answers using a locally running LLM.
- Verify answers against retrieved context.
- Display source document names and page citations.
- Interact with the application through a Streamlit interface and FastAPI backend.

**Technologies**: 
- Python
- FastAPI
- Streamlit 
- Ollama
- Qwen 2.5
- Sentence Transformers
- BM25
- Reciprocal Rank Fusion (RRF)
- Cross-Encoder Reranking
- PyPDF




**How is this project useful?**

This architecture has real-world applications.

**Internal company knowledge assistant**

Employees can ask questions about company policies, documentation, onboarding materials, and internal procedures.

**Research and education assistant**

Students and researchers can query textbooks, research papers, lecture notes, and study materials.

**Legal document assistant**

Legal teams can search contracts, agreements, and case documentation. This would need strict access controls and human review.

**Customer support assistant**

Support teams can retrieve answers from product manuals, troubleshooting guides, and technical documentation.

**Business intelligence assistant**

Teams can query financial reports, business documents, and operational records.

This project covered several important AI engineering concepts.

**Concepts	- What you learned**:

- PDF - processing	Extracting text and preserving page metadata
- Chunking -	Splitting documents into meaningful pieces
- Embeddings - Representing text as numerical vectors
- BM25 -	Traditional keyword-based information retrieval
- Semantic search -	Finding information by meaning
- Hybrid search -	Combining keyword and semantic retrieval
- RRF -	Combining multiple ranked result lists
- Cross-encoder	Reranking - retrieved chunks
- RAG	Grounding LLM - responses in external documents
- Evidence checking -	Rejecting unsupported questions
- Answer verification -	Checking generated answers against context
- Citations	Connecting - answers to source pages
- Ollama -	Running an open-source LLM locally
- FastAPI -	Exposing AI functionality through REST APIs
- Streamlit -	Building an interactive frontend

**Challenges we faced**
- These were some of the most useful learning moments.
- Challenge	What we did
- Claude API cost and access issues	Switched to local Ollama models
- Python 3.13 / PyTorch DLL issue on Windows	Moved development to Colab, then rebuilt locally
- Local model integration	Connected Qwen 2.5 through Ollama
- PDF processing	Extracted text and generated 197 chunks
- Retrieval quality	Combined BM25 and semantic retrieval
- RRF and reranking	Implemented score fusion and cross-encoder ranking
- Irrelevant questions	Introduced an evidence threshold
- LLM-generated citation inconsistency	Moved citation generation to Python
- Different PDF uploads	Added dynamic indexing through FastAPI
- API integration	Connected FastAPI to the RAG engine



The biggest advantage is that users can interact with large collections of information using natural language instead of manually searching through hundreds of pages.
