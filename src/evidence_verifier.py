import re
import math
from difflib import SequenceMatcher


def normalize_text(value):
    if value is None:
        return ""
    value = str(value).lower()
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def similarity_score(a, b):
    a = normalize_text(a)
    b = normalize_text(b)
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def verify_evidence(script_text, findings):
    script_norm = normalize_text(script_text)
    script_lines = [normalize_text(line) for line in script_text.splitlines()]

    for item in findings:
        evidence = item.get("evidence", [])
        if not isinstance(evidence, list):
            evidence = [evidence]

        match_scores = []
        exact_verified = False
        approximate_verified = False

        for ev in evidence:
            ev_norm = normalize_text(ev)
            if not ev_norm:
                continue

            if ev_norm in script_norm:
                exact_verified = True
                match_scores.append(1.0)
                continue

            best = 0.0
            for line in script_lines:
                if not line:
                    continue
                score = similarity_score(ev_norm, line)
                if score > best:
                    best = score

            match_scores.append(best)
            if best >= 0.72:
                approximate_verified = True

        if exact_verified:
            item["evidence_verified"] = True
            item["evidence_status"] = "verified"
            item["evidence_match_score"] = max(match_scores) if match_scores else 0.0
        elif approximate_verified:
            item["evidence_verified"] = True
            item["evidence_status"] = "approximate"
            item["evidence_match_score"] = max(match_scores) if match_scores else 0.0
        else:
            item["evidence_verified"] = False
            item["evidence_status"] = "missing"
            item["evidence_match_score"] = max(match_scores) if match_scores else 0.0
            item["confidence_score"] = round(max(0.0, item.get("confidence_score", 0.5) * 0.6), 2)

    return findings
