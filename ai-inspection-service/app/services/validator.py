from typing import List, Optional
from app.models.schemas import ValidatedRuleViolationFlag

def validate_and_compute_offsets(document_text: str, flags: List[ValidatedRuleViolationFlag]) -> List[dict]:
    validated_flags = []
    for flag in flags:
        passage = flag.passage.strip()

        # 1. Exact Substring Match Check
        start_idx = document_text.find(passage)

        if start_idx == -1:
            print(f"[REJECTED HALLUCINATION]: '{passage} not found in source document.")
            continue
        
        end_idx = start_idx + len(passage)

        # 2. Add computed character offsets to response payload
        flag_dict = flag.model_dump()
        flag_dict["offsets"] = {
            "start": start_idx,
            "end": end_idx
        }

        validated_flags.append(flag_dict)

    return validated_flags