"""
import_jd_skills.py
-------------------
Converts JD Skill Extraction Agent JSON output → skill_framework.json

USAGE:
  python scripts/import_jd_skills.py --input path/to/jd_output.json

The JD agent outputs a list of roles. Each role has:
  - role_title, function, seniority
  - must_have_skills: [{skill, category, level, rationale}]
  - good_to_have_skills: [{skill, category, rationale}]
  - skill_gaps_to_watch: [{skill, note}]

This script normalises them into skill_framework.json under the right function.

FUNCTION CODE MAPPING (edit if your function names differ):
"""

import json
import re
import argparse
from pathlib import Path

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

def map_function(fn_str):
    return FUNCTION_MAP.get(fn_str.lower().strip(), fn_str.upper()[:6])

def map_level(level_str):
    if not level_str:
        return 2
    return LEVEL_MAP.get(level_str.lower(), 2)

def import_roles(input_path, framework_path):
    with open(input_path) as f:
        raw = json.load(f)

    if isinstance(raw, dict) and "roles" in raw:
        roles = raw["roles"]
    elif isinstance(raw, list):
        roles = raw
    elif isinstance(raw, dict) and "role_title" in raw:
        roles = [raw]
    else:
        print("Unrecognised input format. Expected list of roles or {roles: [...]} wrapper.")
        return

    with open(framework_path) as f:
        framework = json.load(f)

    added = 0
    for role in roles:
        fn_code = map_function(role.get("function", "UNKNOWN"))
        role_title = role.get("role_title", "Unknown Role")
        seniority = role.get("seniority", "IC")
        role_slug = slugify(role_title)

        if fn_code not in framework["functions"]:
            framework["functions"][fn_code] = {"roles": {}}
        if "roles" not in framework["functions"][fn_code]:
            framework["functions"][fn_code]["roles"] = {}

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

        gaps_to_watch = []
        for s in role.get("skill_gaps_to_watch", []):
            gaps_to_watch.append({
                "skill_id": f"{fn_code.lower()}_{slugify(s['skill'])}",
                "skill_name": s["skill"],
                "note": s.get("note", ""),
                "type": "emerging"
            })

        framework["functions"][fn_code]["roles"][role_slug] = {
            "role_title": role_title,
            "seniority": seniority,
            "hiring_bar": role.get("hiring_bar", ""),
            "role_summary": role.get("role_summary", ""),
            "must_have_skills": must_have,
            "good_to_have_skills": good_to_have,
            "skill_gaps_to_watch": gaps_to_watch,
            "_imported_from": str(input_path)
        }
        added += 1
        print(f"  [{fn_code}] {role_title} ({seniority}) — {len(must_have)} must-have, {len(good_to_have)} good-to-have")

    from datetime import date
    framework["_meta"]["last_updated"] = str(date.today())
    with open(framework_path, "w") as f:
        json.dump(framework, f, indent=2)

    print(f"\nImported {added} roles into {framework_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import JD skill extraction JSON into skill_framework.json")
    parser.add_argument("--input", required=True, help="Path to JD agent JSON output file")
    parser.add_argument("--framework", default="data/skill_framework.json", help="Path to skill_framework.json")
    args = parser.parse_args()
    import_roles(Path(args.input), Path(args.framework))
