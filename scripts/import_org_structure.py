"""
import_org_structure.py
-----------------------
Paste your team structure data and this script populates org_structure.json and employees.json

USAGE:
  1. Edit the ORG_DATA dict below with your real numbers
  2. python scripts/import_org_structure.py

OR pass a JSON file:
  python scripts/import_org_structure.py --input my_org.json
"""

import json
import argparse
from pathlib import Path
from datetime import date

# ─── PASTE YOUR ORG DATA HERE ─────────────────────────────────────────────────
ORG_DATA = {
    "TECH": {
        "function_name": "Technology",
        "head": "",
        "manager_count": 0,
        "ic_count": 0,
        "kra": "Build and maintain Wiom's core platform, network management systems, and partner-facing tooling",
        "sub_teams": []
    },
    "OPS": {
        "function_name": "Operations",
        "head": "",
        "manager_count": 0,
        "ic_count": 0,
        "kra": "End-to-end field operations, LCO partner management, device swap governance, ISR reduction",
        "sub_teams": []
    },
    "PROD": {
        "function_name": "Product",
        "head": "",
        "manager_count": 0,
        "ic_count": 0,
        "kra": "Define and deliver product roadmap, customer experience, and ISP platform features",
        "sub_teams": []
    },
    "GROWTH": {
        "function_name": "Growth",
        "head": "",
        "manager_count": 0,
        "ic_count": 0,
        "kra": "Customer acquisition, LCO partner onboarding, market expansion",
        "sub_teams": []
    },
    "FIN": {
        "function_name": "Finance",
        "head": "",
        "manager_count": 0,
        "ic_count": 0,
        "kra": "Financial planning, partner billing, compliance, fundraising support",
        "sub_teams": []
    },
    "HR": {
        "function_name": "Human Resources",
        "head": "",
        "manager_count": 0,
        "ic_count": 0,
        "kra": "Talent acquisition, people development, culture, and org effectiveness",
        "sub_teams": []
    },
}

# ─── EMPLOYEE ROSTER (optional) ───────────────────────────────────────────────
EMPLOYEES = [
    # {"name": "Pranav Gupta", "role_title": "Ops Process Lead", "function_code": "OPS", "manager": "Name", "seniority": "IC"}
]

def build_org_structure(org_data, out_path):
    functions = []
    total = 0
    for fn_code, fn in org_data.items():
        size = fn["manager_count"] + fn["ic_count"]
        total += size
        functions.append({
            "function_code": fn_code,
            "function_name": fn["function_name"],
            "head": fn.get("head", ""),
            "manager_count": fn["manager_count"],
            "ic_count": fn["ic_count"],
            "team_size": size,
            "kra": fn.get("kra", ""),
            "sub_teams": fn.get("sub_teams", [])
        })

    structure = {
        "_meta": {
            "description": "Wiom org structure",
            "last_updated": str(date.today()),
            "total_headcount": total
        },
        "functions": functions
    }

    with open(out_path, "w") as f:
        json.dump(structure, f, indent=2)

    print(f"org_structure.json written — {len(functions)} functions, {total} total headcount")
    for fn in functions:
        print(f"   [{fn['function_code']}] {fn['function_name']}: {fn['team_size']} people")

def build_employees(employees, out_path):
    roster = []
    for i, e in enumerate(employees):
        roster.append({
            "employee_id": f"EMP{str(i+1).zfill(4)}",
            "name": e["name"],
            "role_title": e["role_title"],
            "function_code": e["function_code"],
            "manager": e.get("manager", ""),
            "seniority": e.get("seniority", "IC"),
            "assessment_status": "pending",
            "manager_rating_status": "pending"
        })

    with open(out_path, "w") as f:
        json.dump({"employees": roster}, f, indent=2)

    print(f"employees.json written — {len(roster)} employees")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=None, help="Optional JSON file with org data")
    parser.add_argument("--org-out", default="data/org_structure.json")
    parser.add_argument("--emp-out", default="data/employees.json")
    args = parser.parse_args()

    if args.input:
        with open(args.input) as f:
            data = json.load(f)
        org_data = data.get("functions", ORG_DATA)
        employees = data.get("employees", EMPLOYEES)
    else:
        org_data = ORG_DATA
        employees = EMPLOYEES

    build_org_structure(org_data, Path(args.org_out))
    build_employees(employees, Path(args.emp_out))
