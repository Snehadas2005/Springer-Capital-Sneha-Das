from fastapi import status
from fastapi import responses
from google.genai import documents
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types
from app.models.schemas import InspectionRequest, InspectionResponse
from app.services.llm_agent import inspect_document_with_ai
from app.services.validator import validate_and_compute_offsets

load_dotenv()

app = FastAPI(title="Compliance AI Inspection Agent")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

client = genai.Client(api_key=api_key)

@app.post("/inspect", response_model=InspectionResponse)
def inspect_document(payload: InspectionRequest):
    try:
        # 1. Get raw flags from LLM
        raw_flags = inspect_document_with_ai(payload.document_text, client)
        
        # 2. Validate verbatim quotes & compute character offsets
        validated_flags = validate_and_compute_offsets(payload.document_text, raw_flags)
        
        return InspectionResponse(
            status="success",
            flags=validated_flags
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
