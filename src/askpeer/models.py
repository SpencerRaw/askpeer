"""Pydantic models for AskPeer."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Expert(BaseModel):
    id: str
    name: str
    affiliation: str
    domains: list[str] = Field(default_factory=list)
    methods: list[str] = Field(default_factory=list)
    techniques: list[str] = Field(default_factory=list)
    bio: str = ""
    publications_count: int = 0
    h_index: Optional[int] = None
    google_scholar: str = ""
    availability: str = "flexible"
    delivery_modes: list[str] = Field(default_factory=lambda: ["call", "async"])
    profile_text: str = ""  # concatenated text for embedding


class Question(BaseModel):
    id: str
    text: str
    domain: str = ""
    method: str = ""
    technique: str = ""
    depth: str = "troubleshooting"  # beginner / troubleshooting / advanced
    classified_text: str = ""  # enriched text for embedding


class MatchResult(BaseModel):
    expert: Expert
    score: float
    reason: str = ""
