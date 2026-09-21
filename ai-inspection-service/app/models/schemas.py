from pydantic import BaseModel
from typing import List, Optional

class RuleViolationFlag(BaseModel):
    rule_id: str
    passage: str
    reason: str
    severity: str  # HIGH, MEDIUM, LOW

class TextOffset(BaseModel):
    start: int
    end: int

class ValidatedRuleViolationFlag(BaseModel):
    rule_id: str
    passage: str
    reason: str
    severity: str
    offsets: TextOffset

class InspectionRequest(BaseModel):
    document_text: str

class InspectionResponse(BaseModel):
    status: str
    flags: List[ValidatedRuleViolationFlag]