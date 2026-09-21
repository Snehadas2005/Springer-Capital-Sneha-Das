from app.services.validator import validate_and_compute_offsets
from app.models.schemas import RuleViolationFlag

def test_valid_passage_returns_offsets():
    doc_text = "We guarantee Jane Smith an 18% annual return."     
    mock_flag = RuleViolationFlag(
        rule_id="FINRA-2210",
        passage="We guarantee Jane Smith an 18% annual return.",    
        reason="Illegal guarantee",
        severity="HIGH"
    )
    
    result = validate_and_compute_offsets(doc_text, [mock_flag])
    assert len(result) == 1
    assert result[0]["offsets"]["start"] == 0
    assert result[0]["offsets"]["end"] == 45

def test_hallucinated_passage_is_discarded():
    doc_text = "We guarantee Jane Smith an 18% annual return."     
    mock_flag = RuleViolationFlag(
        rule_id="FINRA-2210",
        passage="We promise Jane Smith a 18% return.",
        reason="Illegal guarantee",
        severity="HIGH"
    )
    
    result = validate_and_compute_offsets(doc_text, [mock_flag])
    assert len(result) == 0