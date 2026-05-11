from pydantic import BaseModel
from typing import List


class AnalyzeTextRequest(BaseModel):
    letter_text: str


class AnalyzeTextResponse(BaseModel):
    sender: str
    letter_topic: str
    summary: str
    important_information: List[str]
    deadlines: List[str]
    required_actions: List[str]
    payment_information: List[str]
    unclear_or_risky_parts: List[str]
    next_steps: List[str]
    safety_note: str