from typing import List, Literal, Optional

from pydantic import BaseModel

from app.schemas.common import OutputLanguage


class AnalyzeTextRequest(BaseModel):
    letter_text: str
    output_language: OutputLanguage = "English"


class AnalyzeTextResponse(BaseModel):
    is_valid_letter: bool
    letter_text: str
    confidence_level: str
    confidence_reason: str
    letter_involves_payment: bool
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
    output_language: OutputLanguage = "English"


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
    reply_intent: Optional[str] = None
    output_language: OutputLanguage = "English"

class ChatResponse(BaseModel):
    reply: str
    ui_action: Optional[str] = None
    options: Optional[List[str]] = None

class InvalidLetterResponse(BaseModel):
    is_valid_letter: bool = False
    message: str
