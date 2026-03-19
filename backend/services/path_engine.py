"""
70-20-10 upskilling path generator
Calls Claude to generate personalised, experience-first development plans
"""
import json
from backend.services.claude_client import call_claude
from backend.services.skill_engine import get_employee_gaps

SYSTEM_PROMPT = """You are a senior L&D and OD expert. You generate personalised upskilling paths grounded in the 70-20-10 learning model.

Rules:
- Gap >= 2 levels → MUST include a stretch assignment as the primary intervention
- Gap = 1 level → social learning first (mentor pairing), formal second
- Gap < 1 (exceeds expected) → suggest peer-teaching opportunity to reinforce mastery
- Always surface internal experts: employees at level 3-4 in that skill who could mentor
- Interventions must be realistic for a ~50-person Indian ISP startup
- Prefer on-the-job experiences over external courses wherever possible
- Output ONLY valid JSON, no markdown

Output format:
{
  "employee_id": "...",
  "employee_name": "...",
  "top_3_priorities": [
    {
      "skill_name": "...",
      "gap_score": 1.5,
      "interventions": {
        "experiential_70": "Specific stretch assignment or project ownership recommendation",
        "social_20": "Mentor pairing suggestion or peer learning approach",
        "formal_10": "Specific course/certification only if above two are insufficient"
      },
      "timeline_weeks": 12,
      "success_indicator": "How to know the skill gap is closing"
    }
  ],
  "quick_wins": ["2-3 things the employee can do THIS WEEK"],
  "manager_coaching_prompts": ["2-3 conversation starters for the manager's 1:1"]
}"""


def generate_upskilling_path(employee_id: str, employee_name: str, function_context: str) -> dict:
    gaps = get_employee_gaps(employee_id)
    if not gaps:
        return {"error": "No gap data found. Ensure self-assessment and manager rating are complete."}

    top_gaps = [g for g in gaps if g["gap_score"] > 0][:5]

    user_msg = f"""
Employee: {employee_name} (ID: {employee_id})
Function: {function_context}
Company: Wiom — early-stage ISP operating through LCO partner networks in India, ~50 person team

Top skill gaps (prioritised by business criticality):
{json.dumps(top_gaps, indent=2)}

Generate a personalised 70-20-10 upskilling plan for the top 3 gaps.
Focus on what can be done WITHIN Wiom — stretch assignments, internal mentors, cross-functional projects.
"""
    return call_claude(SYSTEM_PROMPT, user_msg)
