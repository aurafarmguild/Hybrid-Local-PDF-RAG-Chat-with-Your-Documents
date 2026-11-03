
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel

from backend.rag_engine import process_pdf
from backend.retrieval import HybridRetriever
from backend.generator import answer_question


app = FastAPI(
    title="Local PDF RAG API",
    description="A local PDF question-answering system",
    version="1.0.0"
)

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Load the default PDF when the API starts
PDF_PATH = UPLOAD_DIR / "Everything-to-know-about-RAG.pdf"

chunks = process_pdf(str(PDF_PATH))
active_retriever = HybridRetriever(chunks)
active_filename = PDF_PATH.name


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "PDF RAG API is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "active_document": active_filename,
        "chunks": len(chunks)
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global chunks, active_retriever, active_filename

    # Check file extension
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # Create a unique filename
    filename = f"{uuid4().hex}_{Path(file.filename).name}"
    file_path = UPLOAD_DIR / filename

    try:
        # Save uploaded PDF
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        file_path.write_bytes(content)

        # Process the new PDF
        new_chunks = process_pdf(str(file_path))

        if not new_chunks:
            raise ValueError("No readable text found in the PDF.")

        # Build the new retrieval index
        new_retriever = HybridRetriever(new_chunks)

        # Activate the new document only after successful processing
        chunks = new_chunks
        active_retriever = new_retriever
        active_filename = Path(file.filename).name

        return {
            "message": "PDF uploaded and indexed successfully!",
            "filename": active_filename,
            "chunks": len(chunks)
        }

    except HTTPException:
        file_path.unlink(missing_ok=True)
        raise

    except Exception as e:
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500,
            detail=f"PDF processing failed: {str(e)}"
        )

    finally:
        await file.close()


@app.post("/ask")
def ask_question(request: QuestionRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    retrieved_chunks = active_retriever.retrieve(
        request.question,
        candidate_k=20,
        final_k=5
    )

    answer = answer_question(
        request.question,
        retrieved_chunks
    )

    return {
        "question": request.question,
        "answer": answer,
        "document": active_filename
    }
