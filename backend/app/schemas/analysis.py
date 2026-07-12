from typing import Annotated, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.config import MAX_LETTER_TEXT_CHARS
from app.schemas.common import OutputLanguage


AnalysisText = Annotated[str, Field(max_length=10_000)]
AnalysisListItem = Annotated[str, Field(max_length=5_000)]
AnalysisList = Annotated[List[AnalysisListItem], Field(max_length=50)]
SenderType = Literal[
    "Public office",
    "University",
    "Insurance",
    "Bank",
    "Employer",
    "Other",
    "Unknown",
]
UrgencyLevel = Literal["High", "Medium", "Low"]
ConfidenceLevel = Literal["high", "medium", "low"]


class AnalyzeTextRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    letter_text: str = Field(min_length=1, max_length=MAX_LETTER_TEXT_CHARS)
    output_language: OutputLanguage = "English"


class LLMAnalysisResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_valid_letter: bool
    message: AnalysisText
    letter_involves_payment: bool
    sender: AnalysisText
    sender_type: SenderType
    urgency_level: UrgencyLevel
    urgency_reason: AnalysisText
    letter_topic: AnalysisText
    tldr: AnalysisText
    useful_details: AnalysisList
    deadlines: AnalysisList
    required_actions: AnalysisList
    required_documents: AnalysisList
    payment_information: AnalysisList
    possible_consequences: AnalysisList
    unclear_or_risky_parts: AnalysisList
    safety_note: AnalysisText

    @model_validator(mode="after")
    def validate_message(self):
        if self.is_valid_letter and self.message.strip():
            raise ValueError("Valid-letter responses must use an empty message.")
        if not self.is_valid_letter and not self.message.strip():
            raise ValueError("Invalid-letter responses must include a message.")
        return self


class AnalyzeTextResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_valid_letter: bool
    letter_text: str = Field(min_length=1, max_length=MAX_LETTER_TEXT_CHARS)
    confidence_level: ConfidenceLevel
    confidence_reason: AnalysisText
    letter_involves_payment: bool
    sender: AnalysisText
    sender_type: SenderType
    urgency_level: UrgencyLevel
    urgency_reason: AnalysisText
    letter_topic: AnalysisText
    tldr: AnalysisText
    useful_details: AnalysisList
    deadlines: AnalysisList
    required_actions: AnalysisList
    required_documents: AnalysisList
    payment_information: AnalysisList
    possible_consequences: AnalysisList
    unclear_or_risky_parts: AnalysisList
    safety_note: AnalysisText


class FollowUpRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    analysis: AnalyzeTextResponse
    question_type: Literal["payment", "documents", "consequences", "careful"]
    output_language: OutputLanguage = "English"


class FollowUpResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: AnalysisText
    details: List[AnalysisListItem] = Field(max_length=5)


class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=10_000)


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    letter_text: str = Field(min_length=1, max_length=MAX_LETTER_TEXT_CHARS)
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
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    analysis: AnalyzeTextResponse
    intent: ReplyIntent
    additional_context: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=1_000,
    )


class ReplyDraftResponse(BaseModel):
    reply: str = Field(min_length=1, max_length=10_000)


class InvalidLetterResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_valid_letter: Literal[False] = False
    message: str = Field(min_length=1, max_length=2_000)


class TranslateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    analysis: AnalyzeTextResponse
    output_language: OutputLanguage = "English"
