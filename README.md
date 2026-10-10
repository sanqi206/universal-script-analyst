# Universal Script Analyst

A minimal script analysis tool for screenplay QA.

This package is designed to be embedded in Python software.

What it contains
- local lint
- continuity detection
- JSON output schema
- optional OpenAI-based deep analysis
- evidence validation

Project structure
- `src/` contains the Python package logic
- `scripts/` contains CLI entry point
- `examples/` contains test input
- `tests/` contains unit tests

Quick start
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Local mode
```bash
python scripts/analyze_cli.py examples/sample_script.txt --mode local
```

LLM mode
```bash
export OPENAI_API_KEY=your_key_here
python scripts/analyze_cli.py examples/sample_script.txt --mode llm
```

Installation as a package
```bash
pip install -e .
analyze-script examples/sample_script.txt --mode local
```

Usage in software
```python
from src.analyzer import analyze_script

script = """
INT. ROOM - NIGHT
A drinks water.
EXT. STREET - DAY
A is still here.
"""
result = analyze_script(script, title="My Script", fmt="plain", mode="local")
print(result)
```

This is a small practical version.
It is intentionally limited and easy to embed.
