# Universal Script Analyst

A minimal script analysis tool for screenplay QA.

This package is designed to be embedded in Python software.

What it contains
- local lint
- continuity detection
- JSON output schema
- optional OpenAI-based deep analysis
- evidence validation

Quick start
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run local analysis:
```bash
python -c "from src.analyzer import analyze_script; import pathlib; text = pathlib.Path('examples/sample_script.txt').read_text(); print(analyze_script(text, title='demo', fmt='plain', mode='local'))"
```

Run LLM analysis:
```bash
export OPENAI_API_KEY=your_key_here
export ANALYZER_MODE=llm
python -c "from src.analyzer import analyze_script; import pathlib; text = pathlib.Path('examples/sample_script.txt').read_text(); print(analyze_script(text, title='demo', fmt='plain', mode='llm'))"
```

Usage in software:
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
