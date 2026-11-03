
import requests
import re

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"

UNKNOWN_ANSWER = "I don't know based on the uploaded PDF."


def ask_ollama(prompt: str) -> str:
    """Send a prompt to Ollama and return its response."""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        return result["message"]["content"]

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Cannot connect to Ollama. Make sure Ollama is running."
        )

    except requests.exceptions.Timeout:
        raise RuntimeError("Ollama took too long to respond.")

    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"Ollama request failed: {error}")



def has_sufficient_evidence(
    retrieved_chunks: list,
    min_score: float = 0.0
) -> bool:
    """
    Accept the question if at least one retrieved chunk
    has a cross-encoder score >= min_score.
    """

    if not retrieved_chunks:
        print("[DEBUG] No retrieved chunks available.")
        return False

    scores = [
        chunk["rerank_score"]
        for chunk in retrieved_chunks
    ]

    best_score = max(scores)

    print(f"[DEBUG] Best reranker score: {best_score:.4f}")
    print(f"[DEBUG] Required minimum score: {min_score:.4f}")

    if best_score >= min_score:
        print("[DEBUG] Evidence check passed.")
        return True

    print("[DEBUG] Evidence check failed.")
    return False


def format_sources(retrieved_chunks, limit=5):
    seen = set()
    references = []

    for chunk in retrieved_chunks:
        source = chunk["source"]
        page = chunk["page"]

        reference = (source, page)

        if reference not in seen:
            seen.add(reference)
            references.append(
                f"[Source: {source}, Page: {page}]"
            )

        if len(references) >= limit:
            break

    if not references:
        return ""

    return "\n\nSources:\n" + "\n".join(references)

def check_evidence(question: str, context: str) -> bool:
    prompt = f"""
You are checking whether a document contains information relevant
to answering a question.

QUESTION:
{question}

DOCUMENT CONTEXT:
{context}

Decide whether the context contains information that can help answer
the question.

Rules:
- If the context contains relevant information, respond SUPPORT.
- If the context does not contain relevant information, respond INSUFFICIENT.
- Do not use outside knowledge.
- Respond with only one of these words: SUPPORT or INSUFFICIENT.

DECISION:
"""

    result = ask_ollama(prompt).strip().upper()

    print("[DEBUG] Evidence model response:", repr(result))

    # Accept only an explicit SUPPORT classification.
    return result.startswith("SUPPORT")



def generate_answer(question: str, context: str) -> str:
    """Generate an answer using only retrieved PDF context."""

    prompt = f"""
You are a PDF question-answering assistant.

Answer using ONLY the supplied context.

IMPORTANT CITATION RULES:
- Do not include citations in your answer.
- Do not mention page numbers.
- Do not mention source filenames.
- Do not include references or footnotes.
- Python will add source citations separately.
- Do not use outside knowledge.
- Never invent citations.
- If evidence is insufficient, respond exactly:
   {UNKNOWN_ANSWER}

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    return ask_ollama(prompt)


def verify_answer(
    question: str,
    context: str,
    answer: str
) -> bool:
    """Verify whether the generated answer is supported by context."""

    prompt = f"""
You are a strict answer verifier.

Check whether the proposed answer is fully supported
by the supplied context.

Check:
1. Are the factual claims supported?
2. Are the cited source filenames correct?
3. Are the cited page numbers correct?
4. Does the answer introduce unsupported information?

Return only one word:
PASS
or
FAIL

CONTEXT:
{context}

QUESTION:
{question}

PROPOSED ANSWER:
{answer}

DECISION:
"""

    result = ask_ollama(prompt).strip().upper()

    return result.startswith("PASS")


def validate_citations(answer: str, retrieved_chunks: list) -> bool:
    """Ensure citations reference actual retrieved source/page pairs."""

    citations = re.findall(
        r"\[Source:\s*(.*?),\s*Page:\s*(\d+)\]",
        answer
    )

    if not citations:
        return False

    valid_sources = {
        (chunk["source"], str(chunk["page"]))
        for chunk in retrieved_chunks
    }

    for source, page in citations:
        if (source.strip(), page) not in valid_sources:
            return False

    return True



def answer_question(question: str, retrieved_chunks: list) -> str:
    
    if not retrieved_chunks:
        return UNKNOWN_ANSWER

    context_parts = []

    for chunk in retrieved_chunks:
        context_parts.append(
            f"""
Source: {chunk['source']}
Page: {chunk['page']}

Content:
{chunk['text']}
"""
        )

    context = "\n\n".join(context_parts)

    # Evidence check temporarily bypassed.
    print("\n[DEBUG] Checking retrieval evidence...")
    
    if not has_sufficient_evidence(
    retrieved_chunks,min_score=-1.0):
    
        return UNKNOWN_ANSWER

    print("[DEBUG] Generating answer...")
    answer = generate_answer(question, context)
    answer = re.sub(
    r"\s*\[Source:.*?Page:\s*\d+\]",
    "",
    answer
).strip()

    print("[DEBUG] Generated answer:", answer)

    if UNKNOWN_ANSWER.lower() in answer.lower():
        return UNKNOWN_ANSWER

    print("[DEBUG] Verifying answer...")

    if not verify_answer(question, context, answer):
        print("[DEBUG] REJECTED: Answer verification failed.")
        return UNKNOWN_ANSWER

    print("[DEBUG] Answer verification passed.")

    # Generate citations programmatically.
    print("[DEBUG] Adding citations...")

    sources = format_sources(retrieved_chunks, limit=2)

    if not sources:
        return UNKNOWN_ANSWER

    final_answer = answer.strip() + sources

    print("[DEBUG] Citations added successfully.")

    return final_answer

