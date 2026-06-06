from typing import List, Literal

from pydantic import BaseModel


class AnalyzeTextRequest(BaseModel):
    letter_text: str


class AnalyzeTextResponse(BaseModel):
    sender: str
    sender_type: str
    urgency_level: str
    urgency_reason: str
    letter_topic: str
    tldr: str
    useful_details: List[str]
    deadlines: List[str]
    required_actions: List[str]
    required_documents: List[str]
    payment_information: List[str]
    possible_consequences: List[str]
    unclear_or_risky_parts: List[str]
    safety_note: str


class FollowUpRequest(BaseModel):
    analysis: AnalyzeTextResponse
    question_type: Literal["payment", "documents", "consequences", "careful"]


class FollowUpResponse(BaseModel):
    summary: str
    details: List[str]

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    letter_text: str
    analysis: AnalyzeTextResponse
    messages: List[ChatMessage]