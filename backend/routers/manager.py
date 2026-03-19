"""
Manager router — rating and coaching endpoints
"""
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from backend.services.storage import read_json, write_json
from backend.services.skill_engine import get_employee_gaps
from backend.models.schemas import ManagerRatingSubmit

router = APIRouter()


@router.get("/manager/directs/{manager_name}")
def get_directs(manager_name: str):
    """Returns all direct reports for a manager with their status flags."""
    employees_data = read_json("employees.json")
    directs = [
        e for e in employees_data.get("employees", [])
        if manager_name.lower() in e.get("manager", "").lower()
    ]
    if not directs:
        raise HTTPException(
            status_code=404,
            detail=f"No direct reports found for manager '{manager_name}'"
        )
    return {"manager": manager_name, "directs": directs, "count": len(directs)}


@router.get("/manager/rate/{employee_id}")
def get_rating_form(employee_id: str):
    """
    Returns employee self-ratings alongside blank manager rating slots.
    Enables side-by-side comparison in the manager form.
    """
    employees_data = read_json("employees.json")
    employee = next(
        (e for e in employees_data.get("employees", []) if e["employee_id"] == employee_id),
        None
    )
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")

    # Get self-assessment
    assessments = read_json("assessments.json")
    self_data = next(
        (a for a in assessments.get("assessments", []) if a["employee_id"] == employee_id),
        None
    )

    # Get existing manager rating if any
    ratings_data = read_json("manager_ratings.json")
    mgr_data = next(
        (r for r in ratings_data.get("ratings", []) if r["employee_id"] == employee_id),
        None
    )

    return {
        "employee": employee,
        "self_ratings": self_data["ratings"] if self_data else [],
        "manager_ratings": mgr_data["ratings"] if mgr_data else [],
        "self_submitted_at": self_data.get("submitted_at") if self_data else None,
        "assessment_complete": self_data is not None,
        "label_self": "Employee का नज़रिया",
        "label_manager": "आपका आकलन",
    }


@router.post("/manager/rate")
def submit_manager_rating(payload: ManagerRatingSubmit):
    """Upsert manager rating. Updates employee status."""
    now = datetime.now(timezone.utc).isoformat()
    data = read_json("manager_ratings.json")

    data["ratings"] = [
        r for r in data["ratings"] if r["employee_id"] != payload.employee_id
    ]
    data["ratings"].append({
        "manager_id": payload.manager_id,
        "employee_id": payload.employee_id,
        "ratings": [r.model_dump() for r in payload.ratings],
        "coaching_notes": payload.coaching_notes or "",
        "submitted_at": payload.submitted_at or now,
    })
    write_json("manager_ratings.json", data)

    # Update employee status
    employees_data = read_json("employees.json")
    for emp in employees_data["employees"]:
        if emp["employee_id"] == payload.employee_id:
            emp["manager_rating_status"] = "submitted"
            break
    write_json("employees.json", employees_data)

    # Return coaching starters
    gaps = get_employee_gaps(payload.employee_id)
    top_gaps = [g for g in gaps if g["gap_score"] > 0][:3]
    coaching_starters = _generate_coaching_starters(top_gaps)

    return {
        "status": "submitted",
        "message": "Rating saved. यहाँ 1:1 के लिए coaching starters हैं:",
        "coaching_starters": coaching_starters,
        "employee_id": payload.employee_id,
    }


@router.get("/manager/coaching/{employee_id}")
def get_coaching_prompts(employee_id: str):
    """Returns coaching conversation starters from gap data."""
    gaps = get_employee_gaps(employee_id)
    top_gaps = [g for g in gaps if g["gap_score"] > 0][:3]
    return {
        "employee_id": employee_id,
        "coaching_starters": _generate_coaching_starters(top_gaps),
        "top_gaps": top_gaps,
    }


def _generate_coaching_starters(gaps: list) -> list:
    starters = []
    for g in gaps[:3]:
        skill = g["skill_name"]
        gap = g["gap_score"]
        if gap >= 2:
            starters.append(
                f"'{skill}' में हम तुम्हें एक stretch project देना चाहते हैं — "
                f"क्या तुम इसके लिए ready feel कर रहे हो?"
            )
        elif gap >= 1:
            starters.append(
                f"'{skill}' पर तुम्हारा growth potential काफी strong है — "
                f"team में कोई mentor है जिससे तुम सीखना चाहोगे?"
            )
        else:
            starters.append(
                f"'{skill}' में तुम बहुत अच्छे हो — "
                f"क्या तुम junior team members को इसमें guide कर सकते हो?"
            )
    return starters
