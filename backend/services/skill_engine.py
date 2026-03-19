"""
Skill gap scoring engine — triangulated data model
self (40%) + manager (50%) + peer (10%)
"""
import os
import json
import re
from pathlib import Path

DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))


def triangulate(self_score: float, manager_score: float, peer_score: float = None) -> float:
    if peer_score is None:
        # No peer data yet — normalise between self and manager
        return round(self_score * 0.44 + manager_score * 0.56, 2)
    return round(self_score * 0.40 + manager_score * 0.50 + peer_score * 0.10, 2)


def compute_gap(triangulated: float, expected: float, weight: float = 1.0) -> dict:
    gap = round(expected - triangulated, 2)
    priority = round(gap * weight, 2) if gap > 0 else 0
    return {
        "gap_score": gap,
        "priority_score": priority,
        "status": "gap" if gap > 0 else ("met" if gap == 0 else "exceeds")
    }


def get_employee_gaps(employee_id: str) -> list:
    """
    Returns prioritised gap list for one employee.
    Requires self-assessment and manager rating to exist.
    """
    from backend.services.storage import read_json
    assessments = read_json("assessments.json")
    ratings = read_json("manager_ratings.json")
    framework = read_json("skill_framework.json")

    self_data = next((a for a in assessments["assessments"] if a["employee_id"] == employee_id), None)
    mgr_data = next((r for r in ratings["ratings"] if r["employee_id"] == employee_id), None)

    if not self_data:
        return []

    self_map = {r["skill_id"]: r["self_rating"] for r in self_data["ratings"]}
    mgr_map = {r["skill_id"]: r["self_rating"] for r in mgr_data["ratings"]} if mgr_data else {}

    fn_code = self_data["function_code"]
    role_slug = _find_role_slug(self_data["role_title"], framework, fn_code)
    if not role_slug:
        return []

    role = framework["functions"][fn_code]["roles"][role_slug]
    gaps = []

    for skill in role["must_have_skills"] + role["good_to_have_skills"]:
        sid = skill["skill_id"]
        self_score = self_map.get(sid, 0)
        mgr_score = mgr_map.get(sid, self_score)  # fallback to self if no manager rating
        tri = triangulate(self_score, mgr_score)
        gap_data = compute_gap(tri, skill["expected_level"], skill["business_criticality_weight"])
        gaps.append({
            "skill_id": sid,
            "skill_name": skill["skill_name"],
            "category": skill["category"],
            "type": skill["type"],
            "self_score": self_score,
            "manager_score": mgr_score,
            "triangulated_score": tri,
            "expected_level": skill["expected_level"],
            **gap_data
        })

    return sorted(gaps, key=lambda x: x["priority_score"], reverse=True)


def _find_role_slug(role_title: str, framework: dict, fn_code: str) -> str:
    slug = re.sub(r'[^a-z0-9]+', '_', role_title.lower()).strip('_')
    roles = framework.get("functions", {}).get(fn_code, {}).get("roles", {})
    if slug in roles:
        return slug
    # fuzzy: find closest match
    for key in roles:
        if key in slug or slug in key:
            return key
    return None
