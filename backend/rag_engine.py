from pathlib import Path
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def extract_pdf_text(pdf_path: str) -> list:
    """
    Extract text from each PDF page.

    Returns a list of dictionaries containing:
    source, page, and text.
    """

    reader = PdfReader(pdf_path)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text and text.strip():

            documents.append({
                "source": Path(pdf_path).name,
                "page": page_number,
                "text": text.strip()
            })

    return documents


def chunk_documents(documents: list) -> list:
    """
    Split extracted PDF pages into smaller chunks
    while preserving source and page metadata.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = []

    chunk_id = 0

    for document in documents:

        page_chunks = splitter.split_text(document["text"])

        for chunk_number, chunk_text in enumerate(page_chunks, start=1):

            chunks.append({
                "chunk_id": chunk_id,
                "source": document["source"],
                "page": document["page"],
                "chunk_number": chunk_number,
                "text": chunk_text
            })

            chunk_id += 1

    return chunks


def process_pdf(pdf_path: str) -> list:
    """
    Complete PDF processing pipeline:
    extraction followed by chunking.
    """

    documents = extract_pdf_text(pdf_path)

    chunks = chunk_documents(documents)

    return chunks