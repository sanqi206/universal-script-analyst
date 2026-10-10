from openai import OpenAI
from config import CONFIG
from src.prompt_builder import build_prompt

def call_llm(script_text, title="Untitled Script", fmt="plain"):
    if not CONFIG.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set")

    client = OpenAI(api_key=CONFIG.OPENAI_API_KEY)

    system_prompt, user_prompt = build_prompt(script_text, title, fmt)

    response = client.chat.completions.create(
        model=CONFIG.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
        max_tokens=1500
    )

    return response.choices[0].message.content
