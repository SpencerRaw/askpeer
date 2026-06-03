"""Matching engine: question → classification → embedding → similarity.

Uses sklearn TF-IDF for embeddings (no GPU, no model download, fast).
"""

import os
import json
from typing import Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI

from .models import Expert, Question, MatchResult


def _get_api_key():
    return (
        os.environ.get("OPENROUTER_API_KEY")
        or os.environ.get("DEEPSEEK" + "_API_KEY")
        or ""
    )


def _get_client():
    ak = _get_api_key()
    if ak.startswith("sk-or-"):
        return OpenAI(api_key=ak, base_url="https://openrouter.ai/api/v1"), "deepseek/deepseek-chat"
    else:
        return OpenAI(api_key=ak, base_url="https://api.deepseek.com/v1"), "deepseek-chat"


# Global TF-IDF vectorizer (re-fitted per query batch)
_vectorizer: Optional[TfidfVectorizer] = None


def _get_vectorizer() -> TfidfVectorizer:
    return TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000,
    )


def classify_question(question_text: str) -> dict:
    """Use LLM to classify the question into domain/method/technique and enrich it."""
    ak = _get_api_key()
    if not ak:
        return {
            "domain": "",
            "method": "",
            "technique": "",
            "depth": "troubleshooting",
            "classified_text": question_text,
        }

    client, model = _get_client()

    prompt = f"""Analyze this research question and extract structured metadata. Also rewrite it into a keyword-rich paragraph for semantic search.

Question: {question_text}

Output ONLY valid JSON:
{{
  "domain": "primary research domain (e.g., structural biology, organic chemistry)",
  "method": "primary method mentioned (e.g., cryo-EM, molecular dynamics, PCR)",
  "technique": "specific technique (e.g., grid preparation, force field parameterization)",
  "depth": "one of: beginner/troubleshooting/advanced",
  "classified_text": "a keyword-rich 2-3 sentence paragraph expanding the question for embedding search"
}}"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=500,
    )

    result = json.loads(response.choices[0].message.content)
    return result


def _build_expert_text(e: Expert) -> str:
    """Build a rich text representation of an expert for TF-IDF matching."""
    parts = [
        e.name,
        e.affiliation,
        *e.domains,
        *e.methods,
        *e.techniques,
        e.bio,
        e.profile_text,
    ]
    return " ".join(p for p in parts if p)


def match_question_to_experts(
    question: Question,
    experts: list[Expert],
    top_k: int = 3,
    use_llm_rerank: bool = False,
) -> list[MatchResult]:
    """Match a question to the most relevant experts using TF-IDF + cosine similarity."""
    if not experts:
        return []

    query_text = question.classified_text or question.text
    expert_texts = [_build_expert_text(e) for e in experts]

    # Fit TF-IDF on the full corpus (query + all experts)
    vectorizer = _get_vectorizer()
    all_texts = [query_text] + expert_texts
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # First row is query, rest are experts
    query_vec = tfidf_matrix[0:1]
    expert_vecs = tfidf_matrix[1:]

    # Cosine similarity
    similarities = cosine_similarity(query_vec, expert_vecs)[0]
    top_indices = np.argsort(similarities)[-top_k:][::-1]

    results = []
    for idx in top_indices:
        results.append(
            MatchResult(
                expert=experts[idx],
                score=float(similarities[idx]),
                reason=f"Domain match: {', '.join(experts[idx].domains[:3])}",
            )
        )

    if use_llm_rerank and len(results) > 1:
        results = _llm_rerank(question, results)

    return results


def _llm_rerank(question: Question, matches: list[MatchResult]) -> list[MatchResult]:
    """Use LLM to re-rank top matches for better precision."""
    ak = _get_api_key()
    if not ak:
        return matches

    client, model = _get_client()

    experts_str = "\n\n".join(
        f"[{i}] {m.expert.name} ({m.expert.affiliation})\n"
        f"Domains: {', '.join(m.expert.domains)}\n"
        f"Methods: {', '.join(m.expert.methods)}\n"
        f"Bio: {m.expert.bio}"
        for i, m in enumerate(matches)
    )

    prompt = f"""Question: {question.text}

Which of these experts is BEST suited to answer this question? Rank them from most to least relevant.

{experts_str}

Output ONLY a JSON array of indices in order of relevance, e.g. [2, 0, 1]."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=50,
    )

    try:
        order = json.loads(response.choices[0].message.content)
        reranked = [matches[i] for i in order if i < len(matches)]
        return reranked
    except (json.JSONDecodeError, IndexError):
        return matches
