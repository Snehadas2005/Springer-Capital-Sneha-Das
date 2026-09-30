from fastapi import responses
from os import system
import json 
import os
from google import genai
from google.genai import types
from app.models.schemas import ValidatedRuleViolationFlag
from typing import List

def load_compliance_rules():
    """data/rules.json load"""
    rules_path = os.path.join("data", "rules.json")
    if not os.path.exists(rules_path):
        return []
    with open(rules_path, "r", encoding='utf-8') as f:
        return json.load(f)

def inspect_document_with_ai(document_text: str, client: genai.Client) -> List[ValidatedRuleViolationFlag]:
    rules = load_compliance_rules()

    system_instruction = f"""
    You are an expert Compliance Inspection Agent.
    Evaluate the provided document text against these active compliance rules:
    {json.dumps(rules, indent=2)}

    INSTRUCTIONS:
    1. Identify any text passages that violate any of the rules above.
    2. Extract the EXACT quote from the document text for the 'passage' field. Do not paraphrase.
    3. If no rules are violated, return an empty array [].
    """
    # Gemini API Call with Structured Output Enforced
    response = client.models.generate_content(
        model='gemini-3.5-flash-lite',
        contents=document_text,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=list[ValidatedRuleViolationFlag],
            temperature=0.0  # Low temperature for deterministic analysis
        ),
    )

    if not response.text:
        return []

    # Parse JSON into list of RuleViolationFlag objects
    raw_flags = json.loads(response.text)
    return [ValidatedRuleViolationFlag(**flag) for flag in raw_flags]
    