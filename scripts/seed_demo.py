"""
seed_demo.py — Populate all data/ JSON files with realistic Wiom demo data.
Run: python scripts/seed_demo.py
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime, date

DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))

ORG_STRUCTURE = {
    "_meta": {
        "description": "Wiom org structure",
        "last_updated": str(date.today()),
        "total_headcount": 15
    },
    "functions": [
        {"function_code": "TECH", "function_name": "Technology & Engineering", "head_count": 4, "manager_count": 1, "ic_count": 3},
        {"function_code": "OPS", "function_name": "Operations", "head_count": 4, "manager_count": 1, "ic_count": 3},
        {"function_code": "GROWTH", "function_name": "Growth & Sales", "head_count": 3, "manager_count": 1, "ic_count": 2},
        {"function_code": "PROD", "function_name": "Product", "head_count": 2, "manager_count": 1, "ic_count": 1},
        {"function_code": "HR", "function_name": "Human Resources", "head_count": 1, "manager_count": 0, "ic_count": 1},
        {"function_code": "FIN", "function_name": "Finance", "head_count": 1, "manager_count": 0, "ic_count": 1},
    ]
}

SKILL_FRAMEWORK = {
    "_meta": {"last_updated": str(date.today())},
    "functions": {
        "TECH": {
            "roles": {
                "backend_engineer": {
                    "role_title": "Backend Engineer",
                    "seniority": "IC",
                    "must_have_skills": [
                        {"skill_id": "tech_python_backend", "skill_name": "Python / Backend Development", "category": "Technical", "expected_level": 3, "business_criticality_weight": 2.0, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "tech_api_design", "skill_name": "REST API Design", "category": "Technical", "expected_level": 3, "business_criticality_weight": 1.8, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "tech_database", "skill_name": "Database Management (SQL/NoSQL)", "category": "Technical", "expected_level": 2, "business_criticality_weight": 1.5, "strategic_priority": False, "type": "must_have"},
                        {"skill_id": "tech_problem_solving", "skill_name": "Structured Problem Solving", "category": "Behavioural", "expected_level": 3, "business_criticality_weight": 1.5, "strategic_priority": True, "type": "must_have"},
                    ],
                    "good_to_have_skills": [
                        {"skill_id": "tech_system_design", "skill_name": "System Design", "category": "Technical", "expected_level": 2, "business_criticality_weight": 1.2, "strategic_priority": False, "type": "good_to_have"},
                        {"skill_id": "tech_cloud", "skill_name": "Cloud Infrastructure (GCP/AWS)", "category": "Technical", "expected_level": 2, "business_criticality_weight": 1.0, "strategic_priority": False, "type": "good_to_have"},
                    ],
                    "skill_gaps_to_watch": []
                },
                "tech_lead": {
                    "role_title": "Tech Lead",
                    "seniority": "Manager",
                    "must_have_skills": [
                        {"skill_id": "tech_python_backend", "skill_name": "Python / Backend Development", "category": "Technical", "expected_level": 4, "business_criticality_weight": 2.0, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "tech_architecture", "skill_name": "System Architecture", "category": "Technical", "expected_level": 3, "business_criticality_weight": 2.0, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "tech_team_leadership", "skill_name": "Engineering Team Leadership", "category": "Behavioural", "expected_level": 3, "business_criticality_weight": 1.8, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "tech_code_review", "skill_name": "Code Review & Standards", "category": "Technical", "expected_level": 4, "business_criticality_weight": 1.5, "strategic_priority": False, "type": "must_have"},
                    ],
                    "good_to_have_skills": [],
                    "skill_gaps_to_watch": []
                }
            }
        },
        "OPS": {
            "roles": {
                "lco_partner_manager": {
                    "role_title": "LCO Partner Manager",
                    "seniority": "IC",
                    "must_have_skills": [
                        {"skill_id": "ops_partner_mgmt", "skill_name": "LCO Partner Relationship Management", "category": "Domain", "expected_level": 3, "business_criticality_weight": 2.0, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "ops_sla_mgmt", "skill_name": "SLA & KPI Management", "category": "Domain", "expected_level": 2, "business_criticality_weight": 1.8, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "ops_escalation", "skill_name": "Escalation & Conflict Resolution", "category": "Behavioural", "expected_level": 3, "business_criticality_weight": 1.5, "strategic_priority": False, "type": "must_have"},
                        {"skill_id": "ops_field_ops", "skill_name": "Field Operations Coordination", "category": "Domain", "expected_level": 2, "business_criticality_weight": 1.5, "strategic_priority": False, "type": "must_have"},
                    ],
                    "good_to_have_skills": [
                        {"skill_id": "ops_network_basics", "skill_name": "Basic Networking / ISP Knowledge", "category": "Technical", "expected_level": 2, "business_criticality_weight": 1.2, "strategic_priority": False, "type": "good_to_have"},
                        {"skill_id": "ops_data_analysis", "skill_name": "Data Analysis (Excel/Sheets)", "category": "Technical", "expected_level": 2, "business_criticality_weight": 1.0, "strategic_priority": False, "type": "good_to_have"},
                    ],
                    "skill_gaps_to_watch": []
                },
                "ops_head": {
                    "role_title": "Head of Operations",
                    "seniority": "Manager",
                    "must_have_skills": [
                        {"skill_id": "ops_strategic_ops", "skill_name": "Strategic Operations Planning", "category": "Strategic", "expected_level": 3, "business_criticality_weight": 2.0, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "ops_partner_mgmt", "skill_name": "LCO Partner Relationship Management", "category": "Domain", "expected_level": 4, "business_criticality_weight": 2.0, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "ops_team_mgmt", "skill_name": "Team Management", "category": "Behavioural", "expected_level": 3, "business_criticality_weight": 1.8, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "ops_reporting", "skill_name": "Ops Reporting & Dashboards", "category": "Technical", "expected_level": 3, "business_criticality_weight": 1.5, "strategic_priority": False, "type": "must_have"},
                    ],
                    "good_to_have_skills": [],
                    "skill_gaps_to_watch": []
                }
            }
        },
        "GROWTH": {
            "roles": {
                "growth_manager": {
                    "role_title": "Growth Manager",
                    "seniority": "IC",
                    "must_have_skills": [
                        {"skill_id": "growth_lead_gen", "skill_name": "Lead Generation & Pipeline", "category": "Domain", "expected_level": 3, "business_criticality_weight": 2.0, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "growth_onboarding", "skill_name": "Customer Onboarding", "category": "Domain", "expected_level": 3, "business_criticality_weight": 1.8, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "growth_crm", "skill_name": "CRM Usage (Kapture/Salesforce)", "category": "Technical", "expected_level": 2, "business_criticality_weight": 1.5, "strategic_priority": False, "type": "must_have"},
                        {"skill_id": "growth_communication", "skill_name": "Stakeholder Communication", "category": "Behavioural", "expected_level": 3, "business_criticality_weight": 1.5, "strategic_priority": True, "type": "must_have"},
                    ],
                    "good_to_have_skills": [
                        {"skill_id": "growth_analytics", "skill_name": "Growth Analytics & Metrics", "category": "Technical", "expected_level": 2, "business_criticality_weight": 1.2, "strategic_priority": False, "type": "good_to_have"},
                    ],
                    "skill_gaps_to_watch": []
                }
            }
        },
        "PROD": {
            "roles": {
                "product_manager": {
                    "role_title": "Product Manager",
                    "seniority": "Manager",
                    "must_have_skills": [
                        {"skill_id": "prod_roadmap", "skill_name": "Product Roadmapping & Prioritisation", "category": "Strategic", "expected_level": 3, "business_criticality_weight": 2.0, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "prod_user_research", "skill_name": "User Research & Discovery", "category": "Domain", "expected_level": 3, "business_criticality_weight": 1.8, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "prod_data_driven", "skill_name": "Data-Driven Decision Making", "category": "Technical", "expected_level": 3, "business_criticality_weight": 1.8, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "prod_cross_fn", "skill_name": "Cross-functional Collaboration", "category": "Behavioural", "expected_level": 3, "business_criticality_weight": 1.5, "strategic_priority": False, "type": "must_have"},
                    ],
                    "good_to_have_skills": [
                        {"skill_id": "prod_technical", "skill_name": "Technical Product Understanding", "category": "Technical", "expected_level": 2, "business_criticality_weight": 1.2, "strategic_priority": False, "type": "good_to_have"},
                    ],
                    "skill_gaps_to_watch": []
                }
            }
        },
        "HR": {
            "roles": {
                "hr_manager": {
                    "role_title": "HR Manager",
                    "seniority": "IC",
                    "must_have_skills": [
                        {"skill_id": "hr_talent_acq", "skill_name": "Talent Acquisition & Hiring", "category": "Domain", "expected_level": 3, "business_criticality_weight": 1.8, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "hr_perf_mgmt", "skill_name": "Performance Management", "category": "Domain", "expected_level": 3, "business_criticality_weight": 1.8, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "hr_lnd", "skill_name": "Learning & Development", "category": "Domain", "expected_level": 2, "business_criticality_weight": 1.5, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "hr_employee_engagement", "skill_name": "Employee Engagement", "category": "Behavioural", "expected_level": 3, "business_criticality_weight": 1.5, "strategic_priority": False, "type": "must_have"},
                    ],
                    "good_to_have_skills": [
                        {"skill_id": "hr_hris", "skill_name": "HRIS / HR Tools", "category": "Technical", "expected_level": 2, "business_criticality_weight": 1.0, "strategic_priority": False, "type": "good_to_have"},
                    ],
                    "skill_gaps_to_watch": []
                }
            }
        },
        "FIN": {
            "roles": {
                "finance_manager": {
                    "role_title": "Finance Manager",
                    "seniority": "IC",
                    "must_have_skills": [
                        {"skill_id": "fin_financial_analysis", "skill_name": "Financial Analysis & Reporting", "category": "Technical", "expected_level": 3, "business_criticality_weight": 2.0, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "fin_accounting", "skill_name": "Accounting & Compliance", "category": "Domain", "expected_level": 3, "business_criticality_weight": 1.8, "strategic_priority": False, "type": "must_have"},
                        {"skill_id": "fin_cash_flow", "skill_name": "Cash Flow Management", "category": "Domain", "expected_level": 3, "business_criticality_weight": 2.0, "strategic_priority": True, "type": "must_have"},
                        {"skill_id": "fin_excel", "skill_name": "Advanced Excel / Sheets", "category": "Technical", "expected_level": 3, "business_criticality_weight": 1.5, "strategic_priority": False, "type": "must_have"},
                    ],
                    "good_to_have_skills": [
                        {"skill_id": "fin_startup_finance", "skill_name": "Startup Finance / Fundraising Basics", "category": "Strategic", "expected_level": 2, "business_criticality_weight": 1.2, "strategic_priority": False, "type": "good_to_have"},
                    ],
                    "skill_gaps_to_watch": []
                }
            }
        }
    }
}

EMPLOYEES = {
    "employees": [
        {"employee_id": "EMP001", "name": "Rahul Sharma", "role_title": "Tech Lead", "function_code": "TECH", "role_slug": "tech_lead", "manager": "Pranav Chandra", "seniority": "Manager", "email": "rahul@wiom.in", "assessment_status": "pending", "manager_rating_status": "pending"},
        {"employee_id": "EMP002", "name": "Priya Menon", "role_title": "Backend Engineer", "function_code": "TECH", "role_slug": "backend_engineer", "manager": "Rahul Sharma", "seniority": "IC", "email": "priya@wiom.in", "assessment_status": "pending", "manager_rating_status": "pending"},
        {"employee_id": "EMP003", "name": "Amit Kumar", "role_title": "Backend Engineer", "function_code": "TECH", "role_slug": "backend_engineer", "manager": "Rahul Sharma", "seniority": "IC", "email": "amit@wiom.in", "assessment_status": "pending", "manager_rating_status": "pending"},
        {"employee_id": "EMP004", "name": "Deepa Nair", "role_title": "Head of Operations", "function_code": "OPS", "role_slug": "ops_head", "manager": "Pranav Chandra", "seniority": "Manager", "email": "deepa@wiom.in", "assessment_status": "pending", "manager_rating_status": "pending"},
        {"employee_id": "EMP005", "name": "Ravi Patel", "role_title": "LCO Partner Manager", "function_code": "OPS", "role_slug": "lco_partner_manager", "manager": "Deepa Nair", "seniority": "IC", "email": "ravi@wiom.in", "assessment_status": "pending", "manager_rating_status": "pending"},
        {"employee_id": "EMP006", "name": "Sunita Yadav", "role_title": "LCO Partner Manager", "function_code": "OPS", "role_slug": "lco_partner_manager", "manager": "Deepa Nair", "seniority": "IC", "email": "sunita@wiom.in", "assessment_status": "pending", "manager_rating_status": "pending"},
        {"employee_id": "EMP007", "name": "Kiran Reddy", "role_title": "LCO Partner Manager", "function_code": "OPS", "role_slug": "lco_partner_manager", "manager": "Deepa Nair", "seniority": "IC", "email": "kiran@wiom.in", "assessment_status": "pending", "manager_rating_status": "pending"},
        {"employee_id": "EMP008", "name": "Ankit Gupta", "role_title": "Growth Manager", "function_code": "GROWTH", "role_slug": "growth_manager", "manager": "Pranav Chandra", "seniority": "IC", "email": "ankit@wiom.in", "assessment_status": "pending", "manager_rating_status": "pending"},
        {"employee_id": "EMP009", "name": "Neha Singh", "role_title": "Growth Manager", "function_code": "GROWTH", "role_slug": "growth_manager", "manager": "Pranav Chandra", "seniority": "IC", "email": "neha@wiom.in", "assessment_status": "pending", "manager_rating_status": "pending"},
        {"employee_id": "EMP010", "name": "Vikram Joshi", "role_title": "Product Manager", "function_code": "PROD", "role_slug": "product_manager", "manager": "Pranav Chandra", "seniority": "Manager", "email": "vikram@wiom.in", "assessment_status": "pending", "manager_rating_status": "pending"},
        {"employee_id": "EMP011", "name": "Pooja Iyer", "role_title": "HR Manager", "function_code": "HR", "role_slug": "hr_manager", "manager": "Pranav Chandra", "seniority": "IC", "email": "pooja@wiom.in", "assessment_status": "pending", "manager_rating_status": "pending"},
        {"employee_id": "EMP012", "name": "Sanjay Mehta", "role_title": "Finance Manager", "function_code": "FIN", "role_slug": "finance_manager", "manager": "Pranav Chandra", "seniority": "IC", "email": "sanjay@wiom.in", "assessment_status": "pending", "manager_rating_status": "pending"},
    ]
}

# Sample assessments to make the heatmap non-empty
SAMPLE_ASSESSMENTS = {
    "assessments": [
        {
            "employee_id": "EMP002",
            "function_code": "TECH",
            "role_title": "Backend Engineer",
            "role_slug": "backend_engineer",
            "submitted_at": "2025-03-15T10:00:00",
            "ratings": [
                {"skill_id": "tech_python_backend", "skill_name": "Python / Backend Development", "self_rating": 2, "confidence": "medium"},
                {"skill_id": "tech_api_design", "skill_name": "REST API Design", "self_rating": 2, "confidence": "medium"},
                {"skill_id": "tech_database", "skill_name": "Database Management (SQL/NoSQL)", "self_rating": 2, "confidence": "high"},
                {"skill_id": "tech_problem_solving", "skill_name": "Structured Problem Solving", "self_rating": 2, "confidence": "medium"},
                {"skill_id": "tech_system_design", "skill_name": "System Design", "self_rating": 1, "confidence": "low"},
                {"skill_id": "tech_cloud", "skill_name": "Cloud Infrastructure (GCP/AWS)", "self_rating": 1, "confidence": "low"},
            ]
        },
        {
            "employee_id": "EMP005",
            "function_code": "OPS",
            "role_title": "LCO Partner Manager",
            "role_slug": "lco_partner_manager",
            "submitted_at": "2025-03-15T11:00:00",
            "ratings": [
                {"skill_id": "ops_partner_mgmt", "skill_name": "LCO Partner Relationship Management", "self_rating": 2, "confidence": "medium"},
                {"skill_id": "ops_sla_mgmt", "skill_name": "SLA & KPI Management", "self_rating": 1, "confidence": "low"},
                {"skill_id": "ops_escalation", "skill_name": "Escalation & Conflict Resolution", "self_rating": 2, "confidence": "medium"},
                {"skill_id": "ops_field_ops", "skill_name": "Field Operations Coordination", "self_rating": 3, "confidence": "high"},
                {"skill_id": "ops_network_basics", "skill_name": "Basic Networking / ISP Knowledge", "self_rating": 2, "confidence": "medium"},
                {"skill_id": "ops_data_analysis", "skill_name": "Data Analysis (Excel/Sheets)", "self_rating": 1, "confidence": "low"},
            ]
        },
        {
            "employee_id": "EMP006",
            "function_code": "OPS",
            "role_title": "LCO Partner Manager",
            "role_slug": "lco_partner_manager",
            "submitted_at": "2025-03-15T12:00:00",
            "ratings": [
                {"skill_id": "ops_partner_mgmt", "skill_name": "LCO Partner Relationship Management", "self_rating": 3, "confidence": "high"},
                {"skill_id": "ops_sla_mgmt", "skill_name": "SLA & KPI Management", "self_rating": 2, "confidence": "medium"},
                {"skill_id": "ops_escalation", "skill_name": "Escalation & Conflict Resolution", "self_rating": 3, "confidence": "high"},
                {"skill_id": "ops_field_ops", "skill_name": "Field Operations Coordination", "self_rating": 2, "confidence": "medium"},
                {"skill_id": "ops_network_basics", "skill_name": "Basic Networking / ISP Knowledge", "self_rating": 1, "confidence": "low"},
                {"skill_id": "ops_data_analysis", "skill_name": "Data Analysis (Excel/Sheets)", "self_rating": 2, "confidence": "medium"},
            ]
        },
        {
            "employee_id": "EMP008",
            "function_code": "GROWTH",
            "role_title": "Growth Manager",
            "role_slug": "growth_manager",
            "submitted_at": "2025-03-16T09:00:00",
            "ratings": [
                {"skill_id": "growth_lead_gen", "skill_name": "Lead Generation & Pipeline", "self_rating": 2, "confidence": "medium"},
                {"skill_id": "growth_onboarding", "skill_name": "Customer Onboarding", "self_rating": 3, "confidence": "high"},
                {"skill_id": "growth_crm", "skill_name": "CRM Usage (Kapture/Salesforce)", "self_rating": 1, "confidence": "low"},
                {"skill_id": "growth_communication", "skill_name": "Stakeholder Communication", "self_rating": 3, "confidence": "high"},
                {"skill_id": "growth_analytics", "skill_name": "Growth Analytics & Metrics", "self_rating": 1, "confidence": "low"},
            ]
        },
        {
            "employee_id": "EMP011",
            "function_code": "HR",
            "role_title": "HR Manager",
            "role_slug": "hr_manager",
            "submitted_at": "2025-03-16T10:00:00",
            "ratings": [
                {"skill_id": "hr_talent_acq", "skill_name": "Talent Acquisition & Hiring", "self_rating": 3, "confidence": "high"},
                {"skill_id": "hr_perf_mgmt", "skill_name": "Performance Management", "self_rating": 2, "confidence": "medium"},
                {"skill_id": "hr_lnd", "skill_name": "Learning & Development", "self_rating": 1, "confidence": "low"},
                {"skill_id": "hr_employee_engagement", "skill_name": "Employee Engagement", "self_rating": 3, "confidence": "high"},
                {"skill_id": "hr_hris", "skill_name": "HRIS / HR Tools", "self_rating": 2, "confidence": "medium"},
            ]
        },
        {
            "employee_id": "EMP012",
            "function_code": "FIN",
            "role_title": "Finance Manager",
            "role_slug": "finance_manager",
            "submitted_at": "2025-03-16T11:00:00",
            "ratings": [
                {"skill_id": "fin_financial_analysis", "skill_name": "Financial Analysis & Reporting", "self_rating": 3, "confidence": "high"},
                {"skill_id": "fin_accounting", "skill_name": "Accounting & Compliance", "self_rating": 3, "confidence": "high"},
                {"skill_id": "fin_cash_flow", "skill_name": "Cash Flow Management", "self_rating": 2, "confidence": "medium"},
                {"skill_id": "fin_excel", "skill_name": "Advanced Excel / Sheets", "self_rating": 3, "confidence": "high"},
                {"skill_id": "fin_startup_finance", "skill_name": "Startup Finance / Fundraising Basics", "self_rating": 1, "confidence": "low"},
            ]
        },
    ]
}

SAMPLE_MANAGER_RATINGS = {
    "ratings": [
        {
            "manager_id": "Rahul Sharma",
            "employee_id": "EMP002",
            "submitted_at": "2025-03-16T14:00:00",
            "coaching_notes": "Priya shows good analytical thinking but needs to level up on system design. Pair her with senior engineer for 1:1 mentoring.",
            "ratings": [
                {"skill_id": "tech_python_backend", "skill_name": "Python / Backend Development", "self_rating": 2, "confidence": "high"},
                {"skill_id": "tech_api_design", "skill_name": "REST API Design", "self_rating": 2, "confidence": "medium"},
                {"skill_id": "tech_database", "skill_name": "Database Management (SQL/NoSQL)", "self_rating": 2, "confidence": "high"},
                {"skill_id": "tech_problem_solving", "skill_name": "Structured Problem Solving", "self_rating": 3, "confidence": "high"},
            ]
        }
    ]
}


def seed_all():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    files = {
        "org_structure.json": ORG_STRUCTURE,
        "skill_framework.json": SKILL_FRAMEWORK,
        "employees.json": EMPLOYEES,
        "assessments.json": SAMPLE_ASSESSMENTS,
        "manager_ratings.json": SAMPLE_MANAGER_RATINGS,
    }

    for filename, data in files.items():
        path = DATA_DIR / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  OK {filename}")

    # Update employee assessment_status for seeded assessments
    assessed_ids = {a["employee_id"] for a in SAMPLE_ASSESSMENTS["assessments"]}
    rated_ids = {r["employee_id"] for r in SAMPLE_MANAGER_RATINGS["ratings"]}
    emps = EMPLOYEES["employees"]
    for e in emps:
        if e["employee_id"] in assessed_ids:
            e["assessment_status"] = "submitted"
        if e["employee_id"] in rated_ids:
            e["manager_rating_status"] = "submitted"
    with open(DATA_DIR / "employees.json", "w", encoding="utf-8") as f:
        json.dump({"employees": emps}, f, indent=2, ensure_ascii=False)

    print(f"\nSeeded {len(emps)} employees, {len(SAMPLE_ASSESSMENTS['assessments'])} assessments")
    print("Employee IDs for testing:")
    for e in emps:
        print(f"  {e['employee_id']} — {e['name']} ({e['role_title']}, {e['function_code']})")


if __name__ == "__main__":
    print(f"Seeding data to {DATA_DIR.resolve()}...")
    seed_all()
    print("\nDone! Run the app and test with any employee ID above.")
