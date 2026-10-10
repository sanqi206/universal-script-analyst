import jsonschema

SCHEMA = {
    "type": "object",
    "required": ["meta", "findings", "summary"],
    "properties": {
        "meta": {
            "type": "object",
            "required": ["title", "format", "analysis_time"],
            "properties": {
                "title": {"type": "string"},
                "format": {"type": "string"},
                "analysis_time": {"type": "string"},
                "script_length_pages": {"type": "number"},
                "requested_fields": {"type": "array"}
            }
        },
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "category", "severity", "location", "description", "evidence", "remediation", "confidence_score"],
                "properties": {
                    "id": {"type": "string"},
                    "category": {"type": "string"},
                    "severity": {"type": "string"},
                    "location": {"type": "object"},
                    "description": {"type": "string"},
                    "evidence": {"type": "array"},
                    "remediation": {"type": "string"},
                    "confidence_score": {"type": "number"},
                    "tags": {"type": "array"}
                }
            }
        },
        "summary": {
            "type": "object",
            "required": ["top_issues", "overall_confidence", "recommended_actions"],
            "properties": {
                "top_issues": {"type": "array"},
                "overall_confidence": {"type": "number"},
                "recommended_actions": {"type": "string"}
            }
        }
    }
}

def validate_result(data):
    jsonschema.validate(instance=data, schema=SCHEMA)
    return True
