"""Expertise extraction from publications using LLM."""

import os
import json
from openai import OpenAI
from .models import Expert


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


SYSTEM_PROMPT = """You are an expert profiler for academic matching. Given a researcher's biography and publication list, extract a structured expertise profile.

Output ONLY valid JSON with these fields:
{
  "domains": ["list of research domains, max 5"],
  "methods": ["list of methods/approaches used, max 5"],
  "techniques": ["specific techniques, tools, instruments, max 5"],
  "bio": "2-sentence summary of their expertise",
  "profile_text": "a 3-5 sentence paragraph describing their research expertise in natural language — this will be used for semantic search"
}

Be specific and precise. Use standard academic terminology. Avoid vague terms like 'data analysis' — instead say 'Bayesian hierarchical modeling' or 'multivariate regression.'"""


def extract_expertise(name: str, affiliation: str, publications_text: str) -> dict:
    """Extract structured expertise from researcher's publication list."""
    ak = _get_api_key()
    if not ak:
        raise ValueError(
            "No API key set. Export DEEPSEEK" + "_API_KEY or OPENROUTER_API_KEY."
        )

    client, model = _get_client()

    user_prompt = f"""Researcher: {name}
Affiliation: {affiliation}

Publications:
{publications_text[:5000]}

Extract their expertise profile."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
        max_tokens=800,
    )

    result = json.loads(response.choices[0].message.content)
    return result


def create_expert_from_extraction(
    expert_id: str,
    name: str,
    affiliation: str,
    extraction: dict,
    google_scholar: str = "",
) -> Expert:
    """Create Expert model from extraction result."""
    return Expert(
        id=expert_id,
        name=name,
        affiliation=affiliation,
        domains=extraction.get("domains", []),
        methods=extraction.get("methods", []),
        techniques=extraction.get("techniques", []),
        bio=extraction.get("bio", ""),
        google_scholar=google_scholar,
        profile_text=extraction.get("profile_text", ""),
    )
