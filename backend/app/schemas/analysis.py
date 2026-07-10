from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

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
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=10_000)


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    letter_text: str = Field(min_length=1, max_length=100_000)
    analysis: AnalyzeTextResponse
    messages: List[ChatMessage] = Field(min_length=1, max_length=50)
    output_language: OutputLanguage = "English"

    @model_validator(mode="after")
    def require_latest_user_message(self):
        if self.messages[-1].role != "user":
            raise ValueError("The latest chat message must be from the user.")
        return self


ReplyIntent = Literal[
    "already_completed",
    "need_more_time_or_question",
    "disagree",
]


class ReplyDraftRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    analysis: AnalyzeTextResponse
    intent: ReplyIntent


class ReplyDraftResponse(BaseModel):
    reply: str


class InvalidLetterResponse(BaseModel):
    is_valid_letter: bool = False
    message: str


class TranslateRequest(BaseModel):
    analysis: AnalyzeTextResponse
    output_language: OutputLanguage = "English"
