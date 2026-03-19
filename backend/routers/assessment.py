"""
Assessment router — employee self-assessment endpoints
"""
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from backend.services.storage import read_json, write_json
from backend.services.skill_engine import get_employee_gaps
from backend.models.schemas import AssessmentSubmit

router = APIRouter()

# Generic core skills shown when no framework entry exists for the role
GENERIC_CORE_SKILLS = [
    {"skill_id": "core_communication", "skill_name": "Communication", "category": "Behavioural", "type": "core"},
    {"skill_id": "core_problem_solving", "skill_name": "Problem Solving", "category": "Behavioural", "type": "core"},
    {"skill_id": "core_ownership", "skill_name": "Ownership & Accountability", "category": "Behavioural", "type": "core"},
    {"skill_id": "core_collaboration", "skill_name": "Cross-team Collaboration", "category": "Behavioural", "type": "core"},
    {"skill_id": "core_isp_domain", "skill_name": "ISP / Telecom Domain Knowledge", "category": "Domain", "type": "core"},
]


@router.get("/assess/{employee_id}")
def get_assessment_form(
    employee_id: str,
    name: Optional[str] = Query(default=None, description="Search by name instead of ID"),
):
    """
    Returns employee record + skill list for their role.
    Accepts ?name=Pranav for name-based lookup.
    """
    employees_data = read_json("employees.json")
    employees = employees_data.get("employees", [])

    if name:
        matches = [e for e in employees if name.lower() in e["name"].lower()]
        if not matches:
            raise HTTPException(status_code=404, detail=f"No employee found with name containing '{name}'")
        employee = matches[0]
    else:
        employee = next((e for e in employees if e["employee_id"] == employee_id), None)
        if not employee:
            raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")

    # Load skills from framework
    framework = read_json("skill_framework.json")
    fn_code = employee.get("function_code", "")
    role_title = employee.get("role_title", "")

    skills_to_rate = _get_skills_for_role(framework, fn_code, role_title)
    fallback_used = not skills_to_rate
    if fallback_used:
        skills_to_rate = GENERIC_CORE_SKILLS

    return {
        "employee": employee,
        "skills_to_rate": skills_to_rate,
        "skill_count": len(skills_to_rate),
        "why_this_matters": "यह आपकी growth का map है — honest रहें, कोई गलत जवाब नहीं है। आपकी personalized plan तुरंत मिलेगी।",
        "fallback_used": fallback_used,
        "fallback_message": "अभी आपके role की skills नहीं मिलीं — HR से संपर्क करें।" if fallback_used else None,
    }


@router.post("/assess")
def submit_assessment(payload: AssessmentSubmit):
    """
    Upsert self-assessment. Returns gap summary immediately.
    """
    now = datetime.now(timezone.utc).isoformat()
    data = read_json("assessments.json")

    # Upsert — remove old entry if exists
    data["assessments"] = [
        a for a in data["assessments"] if a["employee_id"] != payload.employee_id
    ]
    data["assessments"].append({
        "employee_id": payload.employee_id,
        "function_code": payload.function_code,
        "role_title": payload.role_title,
        "ratings": [r.model_dump() for r in payload.ratings],
        "submitted_at": payload.submitted_at or now,
    })
    write_json("assessments.json", data)

    # Update employee status
    employees_data = read_json("employees.json")
    for emp in employees_data["employees"]:
        if emp["employee_id"] == payload.employee_id:
            emp["assessment_status"] = "submitted"
            break
    write_json("employees.json", employees_data)

    # Return immediate gap preview (change management hook)
    gaps = get_employee_gaps(payload.employee_id)
    top_gaps = [g for g in gaps if g["gap_score"] > 0][:3]

    return {
        "status": "submitted",
        "message": "आपका assessment submit हो गया! नीचे आपकी top priorities हैं।",
        "top_gaps": top_gaps,
        "total_skills_rated": len(payload.ratings),
    }


def _get_skills_for_role(framework: dict, fn_code: str, role_title: str) -> list:
    import re
    slug = re.sub(r'[^a-z0-9]+', '_', role_title.lower()).strip('_')
    roles = framework.get("functions", {}).get(fn_code, {}).get("roles", {})

    role = roles.get(slug)
    if not role:
        for key in roles:
            if key in slug or slug in key:
                role = roles[key]
                break

    if not role:
        return []

    skills = []
    for s in role.get("must_have_skills", []) + role.get("good_to_have_skills", []):
        skills.append({
            "skill_id": s["skill_id"],
            "skill_name": s["skill_name"],
            "category": s.get("category", "Technical"),
            "type": s.get("type", "must_have"),
        })
    return skills
