import os

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    ANALYZER_MODE = os.getenv("ANALYZER_MODE", "local")  # "local" or "llm"

CONFIG = Config()
