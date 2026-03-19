"""
rebuild_data.py - Rebuild employees.json and assessments.json with real role slugs from CSV framework.
"""
import json
from datetime import date

employees = {
  "employees": [
    {"employee_id":"EMP001","name":"Rahul Sharma","role_title":"Senior Backend Engineer","function_code":"TECH","role_slug":"senior_backend_engineer","manager":"Pranav Chandra","seniority":"Lead","email":"rahul@wiom.in","assessment_status":"pending","manager_rating_status":"pending"},
    {"employee_id":"EMP002","name":"Priya Menon","role_title":"Python Developer","function_code":"TECH","role_slug":"python_developer","manager":"Rahul Sharma","seniority":"IC","email":"priya@wiom.in","assessment_status":"submitted","manager_rating_status":"pending"},
    {"employee_id":"EMP003","name":"Amit Kumar","role_title":"Python Developer","function_code":"TECH","role_slug":"python_developer","manager":"Rahul Sharma","seniority":"IC","email":"amit@wiom.in","assessment_status":"pending","manager_rating_status":"pending"},
    {"employee_id":"EMP004","name":"Deepa Nair","role_title":"Head / Lead Analytics","function_code":"TECH","role_slug":"head_lead_analytics","manager":"Pranav Chandra","seniority":"Lead","email":"deepa@wiom.in","assessment_status":"pending","manager_rating_status":"pending"},
    {"employee_id":"EMP005","name":"Ravi Patel","role_title":"Data Analyst","function_code":"TECH","role_slug":"data_analyst","manager":"Deepa Nair","seniority":"IC","email":"ravi@wiom.in","assessment_status":"submitted","manager_rating_status":"pending"},
    {"employee_id":"EMP006","name":"Sunita Yadav","role_title":"Data Analyst","function_code":"TECH","role_slug":"data_analyst","manager":"Deepa Nair","seniority":"IC","email":"sunita@wiom.in","assessment_status":"submitted","manager_rating_status":"pending"},
    {"employee_id":"EMP007","name":"Kiran Reddy","role_title":"Mobile Lead","function_code":"TECH","role_slug":"mobile_lead","manager":"Rahul Sharma","seniority":"Lead","email":"kiran@wiom.in","assessment_status":"pending","manager_rating_status":"pending"},
    {"employee_id":"EMP008","name":"Ankit Gupta","role_title":"Product Manager","function_code":"PROD","role_slug":"product_manager","manager":"Pranav Chandra","seniority":"IC","email":"ankit@wiom.in","assessment_status":"submitted","manager_rating_status":"pending"},
    {"employee_id":"EMP009","name":"Neha Singh","role_title":"Senior Product Manager / Product Manager","function_code":"PROD","role_slug":"senior_product_manager","manager":"Pranav Chandra","seniority":"IC","email":"neha@wiom.in","assessment_status":"pending","manager_rating_status":"pending"},
    {"employee_id":"EMP010","name":"Vikram Joshi","role_title":"Director - Solution Design","function_code":"PROD","role_slug":"director_solution_design","manager":"Pranav Chandra","seniority":"Director","email":"vikram@wiom.in","assessment_status":"pending","manager_rating_status":"pending"},
    {"employee_id":"EMP011","name":"Pooja Iyer","role_title":"Record to Report (R2R)","function_code":"FIN","role_slug":"r2r_finance","manager":"Pranav Chandra","seniority":"IC","email":"pooja@wiom.in","assessment_status":"submitted","manager_rating_status":"pending"},
    {"employee_id":"EMP012","name":"Sanjay Mehta","role_title":"Record to Report (R2R)","function_code":"FIN","role_slug":"r2r_finance","manager":"Pranav Chandra","seniority":"IC","email":"sanjay@wiom.in","assessment_status":"pending","manager_rating_status":"pending"},
  ]
}

with open("data/employees.json","w",encoding="utf-8") as f:
    json.dump(employees,f,indent=2,ensure_ascii=False)
print("employees.json updated - 12 employees")

with open("data/skill_framework.json",encoding="utf-8") as f:
    fw = json.load(f)

def get_must_skills(fn, rs):
    return fw["functions"].get(fn,{}).get("roles",{}).get(rs,{}).get("must_have_skills",[])

def make_ratings(fn, rs, levels):
    skills = get_must_skills(fn, rs)[:len(levels)]
    out = []
    for i,s in enumerate(skills):
        lvl = levels[i]
        conf = ["low","medium","high"][min(lvl-1,2)]
        out.append({"skill_id":s["skill_id"],"skill_name":s["skill_name"],"self_rating":lvl,"confidence":conf})
    return out

assessments = {"assessments":[
    {
        "employee_id":"EMP002","function_code":"TECH","role_title":"Python Developer","role_slug":"python_developer",
        "submitted_at":"2026-03-18T10:00:00",
        "ratings": make_ratings("TECH","python_developer",[2,2,1,2,3,2,1,2,2])
    },
    {
        "employee_id":"EMP005","function_code":"TECH","role_title":"Data Analyst","role_slug":"data_analyst",
        "submitted_at":"2026-03-18T11:00:00",
        "ratings": make_ratings("TECH","data_analyst",[2,1,3,2,2,1,2,2])
    },
    {
        "employee_id":"EMP006","function_code":"TECH","role_title":"Data Analyst","role_slug":"data_analyst",
        "submitted_at":"2026-03-18T12:00:00",
        "ratings": make_ratings("TECH","data_analyst",[1,2,2,1,3,2,1,2])
    },
    {
        "employee_id":"EMP008","function_code":"PROD","role_title":"Product Manager","role_slug":"product_manager",
        "submitted_at":"2026-03-18T09:00:00",
        "ratings": make_ratings("PROD","product_manager",[2,2,1,2,2,3,2,1,2,2])
    },
    {
        "employee_id":"EMP011","function_code":"FIN","role_title":"Record to Report (R2R)","role_slug":"r2r_finance",
        "submitted_at":"2026-03-18T13:00:00",
        "ratings": make_ratings("FIN","r2r_finance",[3,2,2,2,2,2,2,2,2,2])
    },
]}

with open("data/assessments.json","w",encoding="utf-8") as f:
    json.dump(assessments,f,indent=2,ensure_ascii=False)
print(f"assessments.json: {len(assessments['assessments'])} sample assessments with real skill IDs")

# Check skill lookup works
for a in assessments["assessments"]:
    print(f"  {a['employee_id']}: {len(a['ratings'])} skills rated")
print("Done.")
