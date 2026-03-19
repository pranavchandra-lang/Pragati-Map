"""
AI router — Claude-powered analysis endpoints
"""
import os
import json
from typing import Optional
from pathlib import Path
from fastapi import APIRouter, HTTPException, Request, Header
from backend.services.path_engine import generate_upskilling_path
from backend.services.claude_client import call_claude
from backend.services.storage import read_json
from backend.models.schemas import PathRequest

router = APIRouter()


@router.post("/ai/path")
def get_upskilling_path(payload: PathRequest):
    """
    Generate personalised 70-20-10 upskilling path via Claude.
    Result cached to data/paths/{employee_id}.json.
    """
    # Check cache first
    cache_dir = Path(os.getenv("DATA_DIR", "./data")) / "paths"
    cache_file = cache_dir / f"{payload.employee_id}.json"

    if cache_file.exists():
        try:
            with open(cache_file, encoding="utf-8") as f:
                cached = json.load(f)
            return {"source": "cache", "path": cached}
        except Exception:
            pass  # Regenerate if cache is corrupt

    try:
        result = generate_upskilling_path(
            payload.employee_id,
            payload.employee_name,
            payload.function_context,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail={"error": "AI analysis failed", "detail": str(e)})

    if "error" in result:
        raise HTTPException(status_code=422, detail=result)

    # Cache result
    cache_dir.mkdir(parents=True, exist_ok=True)
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return {"source": "generated", "path": result}


@router.post("/ai/heatmap-insights")
def get_heatmap_insights(request: Request, x_admin_key: Optional[str] = Header(default=None)):
    """
    Send heatmap matrix to Claude and return 3 org-level narratives.
    """
    _admin_auth(request, x_admin_key)

    try:
        heatmap_data = read_json("assessments.json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Build a compact summary for Claude
    from backend.routers.admin import get_heatmap
    # We re-use the heatmap logic inline to avoid circular imports
    try:
        employees = read_json("employees.json").get("employees", [])
        framework = read_json("skill_framework.json")
        matrix_summary = f"Total employees: {len(employees)}"
    except Exception:
        matrix_summary = "Data not available"

    system = """You are an organisational development expert. Given a skill heatmap summary from a ~50 person Indian ISP startup called Wiom, return exactly 3 concise insights in JSON:
{
  "biggest_gap": "1-2 sentence insight about the most critical collective skill gap",
  "emerging_risk": "1-2 sentence insight about a risk that will grow if unaddressed",
  "strategic_recommendation": "1-2 sentence actionable recommendation tied to business growth"
}"""

    user_msg = f"Wiom org skill heatmap summary:\n{matrix_summary}\n\nProvide 3 strategic insights for the HRBP and leadership team."

    try:
        result = call_claude(system, user_msg, max_tokens=600)
    except ValueError as e:
        raise HTTPException(status_code=422, detail={"error": "AI analysis failed", "detail": str(e)})

    return result


@router.post("/ai/path/clear-cache/{employee_id}")
def clear_path_cache(employee_id: str):
    """Clear cached path for an employee so it regenerates on next call."""
    cache_file = Path(os.getenv("DATA_DIR", "./data")) / "paths" / f"{employee_id}.json"
    if cache_file.exists():
        cache_file.unlink()
        return {"status": "cleared", "employee_id": employee_id}
    return {"status": "no_cache", "employee_id": employee_id}


def _admin_auth(request: Request, x_admin_key: Optional[str]):
    user = request.session.get("user")
    if user and user.get("role") == "admin":
        return True
    expected = os.getenv("ADMIN_PASSWORD", "changeme")
    if x_admin_key != expected:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    return True
