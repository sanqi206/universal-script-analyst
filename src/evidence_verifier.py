def verify_evidence(script_text, findings):
    text_lower = script_text.lower()
    for item in findings:
        evidence = item.get("evidence", [])
        verified = True
        for ev in evidence:
            if ev.lower() not in text_lower:
                verified = False
                break
        item["evidence_verified"] = verified
        if not verified:
            item["confidence_score"] = round(max(0.0, item.get("confidence_score", 0.5) * 0.6), 2)
    return findings
