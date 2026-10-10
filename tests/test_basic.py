import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.evidence_verifier import verify_evidence


def test_exact_match_verifies_evidence():
    script = """
    INT. APARTMENT - NIGHT
    JOHN sits at the table with a cup of coffee.
    JOHN
    I am leaving.
    """
    findings = [{
        "id": "F-1",
        "category": "continuity",
        "severity": "high",
        "description": "night-day continuity issue",
        "evidence": ["night", "day"],
        "remediation": "clarify time",
        "confidence_score": 0.9,
    }]
    result = verify_evidence(script, findings)
    assert result[0]["evidence_verified"] is True
    assert result[0]["evidence_status"] in {"verified", "approximate"}


def test_approximate_match_verifies_evidence():
    script = """
    EXT. STREET - DAY
    JOHN walks outside wearing the same coat and holding the same cup.
    """
    findings = [{
        "id": "F-2",
        "category": "continuity",
        "severity": "medium",
        "description": "costume continuity",
        "evidence": ["same jacket"],
        "remediation": "check wardrobe",
        "confidence_score": 0.8,
    }]
    result = verify_evidence(script, findings)
    assert result[0]["evidence_verified"] is True
    assert result[0]["evidence_status"] in {"verified", "approximate"}


def test_missing_evidence_is_flagged():
    script = """
    INT. CAR - NIGHT
    THEY drive in silence.
    """
    findings = [{
        "id": "F-3",
        "category": "logic",
        "severity": "medium",
        "description": "missing explanation",
        "evidence": ["the sun rises"],
        "remediation": "add explanation",
        "confidence_score": 0.7,
    }]
    result = verify_evidence(script, findings)
    assert result[0]["evidence_verified"] is False
    assert result[0]["evidence_status"] == "missing"
