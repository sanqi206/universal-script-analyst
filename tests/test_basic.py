import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.analyzer import analyze_script

def test_basic():
    text = """
    INT. APARTMENT - NIGHT
    JOHN sits at the table with a cup of coffee.
    JOHN
    I am leaving.

    EXT. STREET - DAY
    JOHN walks outside wearing the same coat and holding the same cup.
    """
    result = analyze_script(text, title="demo", fmt="plain", mode="local")
    assert "meta" in result
    assert "findings" in result
    assert "summary" in result
    assert any(f["category"] == "continuity" for f in result["findings"])
