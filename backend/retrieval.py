
import re
import numpy as np
import torch

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, CrossEncoder


# Models used in the original Colab project
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"

RRF_K = 60


def tokenize(text: str) -> list:
    """Simple lowercase tokenizer for BM25."""
    return re.findall(r"\b\w+\b", text.lower())


class HybridRetriever:

    def __init__(self, chunks: list):

        if not chunks:
            raise ValueError("No document chunks were provided.")

        self.chunks = chunks

        # Automatically select GPU if available, otherwise CPU
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Loading retrieval models on: {self.device}")

        # 1. BM25 keyword index
        tokenized_chunks = [
            tokenize(chunk["text"])
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(tokenized_chunks)

        # 2. Semantic embedding model
        self.embedding_model = SentenceTransformer(
            EMBEDDING_MODEL,
            device=self.device
        )

        print("Generating document embeddings...")

        self.embeddings = self.embedding_model.encode(
            [chunk["text"] for chunk in chunks],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        # 3. Cross-encoder reranker
        self.reranker = CrossEncoder(
            RERANKER_MODEL,
            device=self.device
        )

        print("Hybrid retriever is ready!")

    def retrieve(
        self,
        query: str,
        candidate_k: int = 20,
        final_k: int = 5
    ) -> list:
        """
        BM25 + semantic search + RRF + cross-encoder reranking.
        """

        if not query.strip():
            return []

        total_chunks = len(self.chunks)
        candidate_k = min(candidate_k, total_chunks)

        # --------------------------------
        # 1. BM25 keyword search
        # --------------------------------

        query_tokens = tokenize(query)

        bm25_scores = self.bm25.get_scores(query_tokens)

        bm25_ranked = np.argsort(
            bm25_scores
        )[::-1][:candidate_k]

        # --------------------------------
        # 2. Semantic search
        # --------------------------------

        query_embedding = self.embedding_model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )[0]

        semantic_scores = self.embeddings @ query_embedding

        semantic_ranked = np.argsort(
            semantic_scores
        )[::-1][:candidate_k]

        # --------------------------------
        # 3. Reciprocal Rank Fusion
        # --------------------------------

        rrf_scores = {}

        for ranked_list in [bm25_ranked, semantic_ranked]:

            for rank, chunk_index in enumerate(ranked_list, start=1):

                rrf_scores[chunk_index] = (
                    rrf_scores.get(chunk_index, 0)
                    + 1 / (RRF_K + rank)
                )

        rrf_ranked = sorted(
            rrf_scores,
            key=rrf_scores.get,
            reverse=True
        )[:candidate_k]

        # --------------------------------
        # 4. Cross-encoder reranking
        # --------------------------------

        pairs = [
            [query, self.chunks[index]["text"]]
            for index in rrf_ranked
        ]

        rerank_scores = self.reranker.predict(pairs)

        reranked = sorted(
            zip(rrf_ranked, rerank_scores),
            key=lambda item: float(item[1]),
            reverse=True
        )

        # --------------------------------
        # 5. Return final top-k chunks
        # --------------------------------

        results = []

        for chunk_index, score in reranked[:final_k]:

            result = self.chunks[chunk_index].copy()

            result["rrf_score"] = rrf_scores[chunk_index]
            result["rerank_score"] = float(score)

            results.append(result)

        return results
