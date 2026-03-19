"""
Admin router — heatmap, gaps, employee list, framework
All endpoints require X-Admin-Key header OR admin session.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Request, Header
from backend.services.storage import read_json, write_json
from backend.services.skill_engine import get_employee_gaps
import os

router = APIRouter()

CATEGORIES = ["Technical", "Behavioural", "Domain", "Strategic"]


def _admin_auth(request: Request, x_admin_key: Optional[str]):
    """Accept either session-based admin or X-Admin-Key header."""
    user = request.session.get("user")
    if user and user.get("role") == "admin":
        return True
    expected = os.getenv("ADMIN_PASSWORD", "changeme")
    if x_admin_key != expected:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    return True


@router.get("/admin/heatmap")
def get_heatmap(request: Request, x_admin_key: Optional[str] = Header(default=None)):
    _admin_auth(request, x_admin_key)

    employees_data = read_json("employees.json")
    employees = employees_data.get("employees", [])
    assessments = read_json("assessments.json")
    framework = read_json("skill_framework.json")

    assessed_ids = {a["employee_id"] for a in assessments.get("assessments", [])}
    assessed_count = len(assessed_ids)

    gap_accumulator: dict = {}
    worst: dict = {}

    for emp in employees:
        eid = emp["employee_id"]
        fn = emp.get("function_code", "UNKNOWN")
        if eid not in assessed_ids:
            continue

        gaps = get_employee_gaps(eid)
        if fn not in gap_accumulator:
            gap_accumulator[fn] = {cat: [] for cat in CATEGORIES}

        for g in gaps:
            if g["gap_score"] <= 0:
                continue
            cat = g.get("category", "Technical")
            if cat in gap_accumulator[fn]:
                gap_accumulator[fn][cat].append(g["gap_score"])
            key = (fn, g["skill_name"])
            worst.setdefault(key, []).append(g["gap_score"])

    matrix = {}
    for fn, cats in gap_accumulator.items():
        matrix[fn] = {
            cat: round(sum(scores) / len(scores), 2) if scores else 0.0
            for cat, scores in cats.items()
        }

    worst_gaps = sorted(
        [{"function": k[0], "skill": k[1], "avg_gap": round(sum(v)/len(v), 2)} for k, v in worst.items()],
        key=lambda x: x["avg_gap"],
        reverse=True
    )[:5]

    functions_in_matrix = list(matrix.keys()) or [
        f["function_code"] for f in read_json("org_structure.json").get("functions", [])
    ]

    return {
        "functions": functions_in_matrix,
        "categories": CATEGORIES,
        "matrix": matrix,
        "worst_gaps": worst_gaps,
        "assessed_count": assessed_count,
        "total_count": len(employees),
    }


@router.get("/admin/gaps/{employee_id}")
def get_employee_gap_report(employee_id: str, request: Request, x_admin_key: Optional[str] = Header(default=None)):
    _admin_auth(request, x_admin_key)
    gaps = get_employee_gaps(employee_id)
    if gaps is None:
        raise HTTPException(status_code=404, detail=f"No assessment data for {employee_id}")
    return {"employee_id": employee_id, "gaps": gaps, "count": len(gaps)}


@router.get("/admin/employees")
def list_employees(request: Request, x_admin_key: Optional[str] = Header(default=None)):
    _admin_auth(request, x_admin_key)
    data = read_json("employees.json")
    return {"employees": data.get("employees", []), "count": len(data.get("employees", []))}


@router.get("/admin/framework")
def get_framework(request: Request, x_admin_key: Optional[str] = Header(default=None)):
    _admin_auth(request, x_admin_key)
    return read_json("skill_framework.json")


@router.put("/admin/framework/skill/{skill_id}")
def update_skill(
    skill_id: str,
    body: dict,
    request: Request,
    x_admin_key: Optional[str] = Header(default=None),
):
    _admin_auth(request, x_admin_key)
    framework = read_json("skill_framework.json")

    updated = False
    allowed_fields = {"expected_level", "business_criticality_weight", "strategic_priority"}

    for fn_data in framework.get("functions", {}).values():
        for role_data in fn_data.get("roles", {}).values():
            for skill_list_key in ("must_have_skills", "good_to_have_skills"):
                for skill in role_data.get(skill_list_key, []):
                    if skill.get("skill_id") == skill_id:
                        for field in allowed_fields:
                            if field in body:
                                skill[field] = body[field]
                        updated = True

    if not updated:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' not found in framework")

    write_json("skill_framework.json", framework)
    return {"status": "updated", "skill_id": skill_id}


@router.post("/admin/seed")
def seed_demo_data(request: Request, x_admin_key: Optional[str] = Header(default=None)):
    """Seed all data files with realistic Wiom demo data. Idempotent."""
    _admin_auth(request, x_admin_key)
    import sys, importlib
    from pathlib import Path
    # Run the seed script inline
    seed_path = Path(__file__).parents[2] / "scripts" / "seed_demo.py"
    import importlib.util
    spec = importlib.util.spec_from_file_location("seed_demo", seed_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.seed_all()
    return {"status": "seeded", "message": "Demo data loaded. Check /api/v1/admin/employees for employee list."}


@router.post("/admin/import-framework")
def import_framework_from_json(
    payload: dict,
    request: Request,
    x_admin_key: Optional[str] = Header(default=None),
):
    """
    Import JD skill extraction JSON directly into skill_framework.json.
    Accepts the JD agent output format: list of roles OR {roles: [...]} wrapper.
    """
    _admin_auth(request, x_admin_key)

    import re
    from datetime import date

    FUNCTION_MAP = {
        "tech": "TECH", "technology": "TECH", "engineering": "TECH",
        "ops": "OPS", "operations": "OPS",
        "product": "PROD", "prod": "PROD",
        "growth": "GROWTH", "sales": "GROWTH", "marketing": "GROWTH",
        "finance": "FIN", "fin": "FIN",
        "hr": "HR", "human resources": "HR", "people": "HR",
        "strategy": "STRAT", "analytics": "ANALYTICS",
    }
    LEVEL_MAP = {
        "beginner": 1, "awareness": 1,
        "intermediate": 2, "working": 2,
        "advanced": 3, "practitioner": 3,
        "expert": 4,
    }

    def slugify(text):
        return re.sub(r'[^a-z0-9]+', '_', text.lower()).strip('_')

    def map_fn(fn_str):
        return FUNCTION_MAP.get(fn_str.lower().strip(), fn_str.upper()[:8])

    def map_level(level_str):
        if not level_str:
            return 2
        return LEVEL_MAP.get(str(level_str).lower(), 2)

    if isinstance(payload, dict) and "roles" in payload:
        roles = payload["roles"]
    elif isinstance(payload, list):
        roles = payload
    elif isinstance(payload, dict) and "role_title" in payload:
        roles = [payload]
    else:
        raise HTTPException(status_code=422, detail="Expected list of roles or {roles: [...]} wrapper")

    framework = read_json("skill_framework.json")
    added = 0

    for role in roles:
        fn_code = map_fn(role.get("function", "UNKNOWN"))
        role_title = role.get("role_title", "Unknown Role")
        role_slug = slugify(role_title)

        if fn_code not in framework["functions"]:
            framework["functions"][fn_code] = {"roles": {}}

        must_have = []
        for s in role.get("must_have_skills", []):
            must_have.append({
                "skill_id": f"{fn_code.lower()}_{slugify(s['skill'])}",
                "skill_name": s["skill"],
                "category": s.get("category", "Technical"),
                "expected_level": map_level(s.get("level")),
                "business_criticality_weight": 1.5,
                "strategic_priority": False,
                "rationale": s.get("rationale", ""),
                "type": "must_have"
            })

        good_to_have = []
        for s in role.get("good_to_have_skills", []):
            good_to_have.append({
                "skill_id": f"{fn_code.lower()}_{slugify(s['skill'])}",
                "skill_name": s["skill"],
                "category": s.get("category", "Technical"),
                "expected_level": 2,
                "business_criticality_weight": 1.0,
                "strategic_priority": False,
                "rationale": s.get("rationale", ""),
                "type": "good_to_have"
            })

        framework["functions"][fn_code]["roles"][role_slug] = {
            "role_title": role_title,
            "seniority": role.get("seniority", "IC"),
            "must_have_skills": must_have,
            "good_to_have_skills": good_to_have,
            "skill_gaps_to_watch": [],
        }
        added += 1

    framework["_meta"]["last_updated"] = str(date.today())
    write_json("skill_framework.json", framework)

    return {
        "status": "imported",
        "roles_added": added,
        "functions": list(framework["functions"].keys()),
        "message": f"Imported {added} roles. Heatmap will now show data."
    }
