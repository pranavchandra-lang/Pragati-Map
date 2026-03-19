"""
AI wrapper — uses Google Gemini (free tier: gemini-1.5-flash)
All callers use call_claude() — name kept for import compatibility.
"""
import os
import json
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-1.5-pro-latest"


def call_claude(system_prompt: str, user_message: str, max_tokens: int = 4000) -> dict:
    """
    Call Gemini and return parsed JSON. Raises ValueError on parse failure.
    Function name kept as call_claude for import compatibility.
    """
    model = genai.GenerativeModel(
        MODEL,
        system_instruction=system_prompt,
        generation_config=genai.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=0.4,
        ),
    )
    response = model.generate_content(user_message)
    raw = response.text.strip()

    # Strip markdown fences + extract outermost JSON object
    clean = raw.replace("```json", "").replace("```", "").strip()
    first = clean.find("{")
    last = clean.rfind("}")
    if first != -1 and last != -1:
        clean = clean[first:last+1]

    try:
        return json.loads(clean)
    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini returned invalid JSON: {e}\nRaw: {raw[:300]}")
