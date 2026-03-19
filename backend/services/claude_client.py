"""
AI wrapper — calls Gemini REST API directly (v1 endpoint, AI Studio free tier compatible).
Function name kept as call_claude() for import compatibility.
"""
import os
import json
import httpx

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = "gemini-1.5-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent"


def call_claude(system_prompt: str, user_message: str, max_tokens: int = 4000) -> dict:
    """
    Call Gemini v1 REST API and return parsed JSON.
    Raises ValueError on failure or JSON parse error.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")

    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"parts": [{"text": user_message}]}],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": 0.4,
        },
    }

    try:
        resp = httpx.post(
            API_URL,
            params={"key": GEMINI_API_KEY},
            json=payload,
            timeout=30.0,
        )
    except httpx.TimeoutException:
        raise ValueError("Gemini API request timed out.")

    if resp.status_code != 200:
        try:
            err = resp.json()
            msg = err.get("error", {}).get("message", resp.text[:200])
        except Exception:
            msg = resp.text[:200]
        raise ValueError(f"Gemini API error {resp.status_code}: {msg}")

    try:
        raw = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError) as e:
        raise ValueError(f"Unexpected Gemini response structure: {e}")

    # Strip markdown fences and extract JSON
    clean = raw.replace("```json", "").replace("```", "").strip()
    first = clean.find("{")
    last = clean.rfind("}")
    if first != -1 and last != -1:
        clean = clean[first:last + 1]

    try:
        return json.loads(clean)
    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini returned invalid JSON: {e}\nRaw: {raw[:300]}")
