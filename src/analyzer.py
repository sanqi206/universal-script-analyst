import json
import re
import uuid
from datetime import datetime

from config import CONFIG
from src.schema_validator import validate_result
from src.evidence_verifier import verify_evidence
from src.llm_client import call_llm

def normalize(text):
    return text.replace("\r\n", "\n")

def split_scenes(text):
    lines = normalize(text).splitlines()
    scenes = []
    current = []
    current_name = None
    for line in lines:
        if re.match(r'^\s*(INT\.|EXT\.|INT/EXT\.|EST\.)', line, re.I):
            if current:
                scenes.append({"id": current_name or f"SCENE-{len(scenes)+1}", "text": "\n".join(current)})
            current = [line]
            current_name = line.strip()
        else:
            current.append(line)
    if current:
        scenes.append({"id": current_name or f"SCENE-{len(scenes)+1}", "text": "\n".join(current)})
    return scenes

def find_time_jump(text):
    lower = text.lower()
    if (" night" in lower or "night" in lower) and (" day" in lower or "day" in lower):
        return [{
            "id": f"F-{uuid.uuid4().hex[:8]}",
            "category": "continuity",
            "severity": "high",
            "location": {"scene_id": "multiple", "line_range": "scene-level", "page": 0},
            "description": "The script contains both NIGHT and DAY references without a clear transition.",
            "evidence": ["night", "day"],
            "remediation": "Add an explicit transition or clarify the timeline jump.",
            "confidence_score": 0.92,
            "tags": ["time", "continuity"]
        }]
    return []

def find_long_lines(text):
    findings = []
    lines = normalize(text).splitlines()
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if len(s) > 180:
            findings.append({
                "id": f"F-{uuid.uuid4().hex[:8]}",
                "category": "format",
                "severity": "medium",
                "location": {"scene_id": "unknown", "line_range": f"L{i}", "page": 0},
                "description": "This line is unusually long and may indicate formatting or readability issues.",
                "evidence": [s[:200]],
                "remediation": "Break the line into shorter action or dialogue lines.",
                "confidence_score": 0.82,
                "tags": ["format", "readability"]
            })
    return findings

def analyze_local(script_text, title="Untitled Script", fmt="plain"):
    findings = []
    for scene in split_scenes(script_text):
        findings.extend(find_time_jump(scene["text"]))
        findings.extend(find_long_lines(scene["text"]))

    priority = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    findings = sorted(findings, key=lambda x: priority.get(x.get("severity", "low"), 1), reverse=True)

    result = {
        "meta": {
            "title": title,
            "format": fmt,
            "analysis_time": datetime.utcnow().isoformat() + "Z",
            "script_length_pages": round(len(script_text.split()) / 250, 2),
            "requested_fields": []
        },
        "findings": findings,
        "summary": {
            "top_issues": [f["id"] for f in findings[:5]],
            "overall_confidence": round(sum(f.get("confidence_score", 0) for f in findings) / max(len(findings), 1), 2),
            "recommended_actions": "Fix high-severity continuity and format issues before further review."
        }
    }
    return result

def analyze_llm(script_text, title="Untitled Script", fmt="plain"):
    try:
        content = call_llm(script_text, title, fmt)
        data = json.loads(content)
        if "meta" not in data or "findings" not in data or "summary" not in data:
            raise ValueError("LLM returned incomplete JSON")
        data["findings"] = verify_evidence(script_text, data.get("findings", []))
        validate_result(data)
        return data
    except Exception:
        return analyze_local(script_text, title, fmt)

def analyze_script(script_text, title="Untitled Script", fmt="plain", mode="local"):
    if mode == "llm":
        return analyze_llm(script_text, title, fmt)
    return analyze_local(script_text, title, fmt)
