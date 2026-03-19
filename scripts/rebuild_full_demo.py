#!/usr/bin/env python3
"""
Rebuild all demo data for Pragati Map — full org coverage.
Generates skill framework, employees, assessments, and manager ratings
for all 17 Wiom functions.

Run from project root:  python scripts/rebuild_full_demo.py
"""
import json, random, os, sys
from pathlib import Path
from datetime import datetime, timedelta

random.seed(42)

DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

BASE_DATE = datetime(2026, 3, 1)
def ts(days_ago=0):
    return (BASE_DATE - timedelta(days=days_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")

# ─── skill shorthand ──────────────────────────────────────────────────────────
def sk(sid, name, cat, exp, w=1.0, strat=False, rationale="", stype="must_have"):
    return {"skill_id": sid, "skill_name": name, "category": cat,
            "expected_level": exp, "business_criticality_weight": w,
            "strategic_priority": strat, "rationale": rationale, "type": stype}

def gth(sid, name, cat, exp, w=1.0):
    return sk(sid, name, cat, exp, w, False, "", "good_to_have")

# ─── NEW FUNCTION SKILLS ──────────────────────────────────────────────────────
NEW_FUNCTIONS = {
    "EXE": {"roles": {
        "execution_manager": {"role_title": "Execution Manager", "seniority": "Lead",
            "must_have_skills": [
                sk("exe_project_tracking","Project tracking (Jira/Asana)","Technical",3,1.5),
                sk("exe_kpi_dashboards","KPI dashboard management","Technical",3,1.5,True),
                sk("exe_sop_development","SOP development","Technical",3,1.0),
                sk("exe_cross_fn_coord","Cross-functional coordination","Behavioural",3,2.0,True),
                sk("exe_prioritization","Prioritization under pressure","Behavioural",3,1.5),
                sk("exe_stakeholder_mgmt","Stakeholder management","Behavioural",3,1.5),
                sk("exe_lco_knowledge","LCO partner operations","Domain",2,1.5),
                sk("exe_okr_execution","OKR setting and execution","Strategic",3,2.0,True),
                sk("exe_business_planning","Business planning","Strategic",3,1.5,True),
            ],
            "good_to_have_skills": [
                gth("exe_process_automation","Process automation","Technical",2,1.0),
                gth("exe_change_mgmt","Change management","Behavioural",2,1.0),
            ]},
        "operations_analyst": {"role_title": "Operations Analyst", "seniority": "IC",
            "must_have_skills": [
                sk("exe_project_tracking","Project tracking (Jira/Asana)","Technical",2,1.5),
                sk("exe_kpi_dashboards","KPI dashboard management","Technical",2,1.5),
                sk("exe_sop_development","SOP development","Technical",2,1.0),
                sk("exe_cross_fn_coord","Cross-functional coordination","Behavioural",2,1.5),
                sk("exe_prioritization","Prioritization under pressure","Behavioural",2,1.5),
                sk("exe_lco_knowledge","LCO partner operations","Domain",2,1.5),
                sk("exe_regulatory_compliance","Regulatory compliance basics","Domain",2,1.0),
            ],
            "good_to_have_skills": [
                gth("exe_data_analysis","Data analysis (Excel/Sheets)","Technical",2,1.0),
                gth("exe_stakeholder_mgmt","Stakeholder communication","Behavioural",2,1.0),
            ]},
    }},
    "CX": {"roles": {
        "cx_team_lead": {"role_title": "CX Team Lead", "seniority": "Lead",
            "must_have_skills": [
                sk("cx_crm_tools","CRM tools (Freshdesk/Zoho)","Technical",3,1.5),
                sk("cx_sla_tracking","SLA tracking and reporting","Technical",3,1.5,True),
                sk("cx_nps_measurement","NPS measurement","Technical",3,2.0,True),
                sk("cx_customer_empathy","Customer empathy","Behavioural",3,2.0),
                sk("cx_conflict_resolution","Conflict resolution","Behavioural",3,1.5),
                sk("cx_team_coaching","Team coaching","Behavioural",3,1.5),
                sk("cx_isp_service","ISP service knowledge","Domain",3,1.5),
                sk("cx_escalation_protocols","Escalation protocols","Domain",3,1.5),
                sk("cx_nps_strategy","NPS improvement strategy","Strategic",3,2.0,True),
                sk("cx_retention_planning","Customer retention planning","Strategic",3,1.5,True),
            ],
            "good_to_have_skills": [
                gth("cx_multilingual","Multilingual support","Behavioural",2,0.8),
                gth("cx_cx_roadmap","CX roadmap ownership","Strategic",2,1.0),
            ]},
        "customer_support_exec": {"role_title": "Customer Support Executive", "seniority": "IC",
            "must_have_skills": [
                sk("cx_crm_tools","CRM tools (Freshdesk/Zoho)","Technical",2,1.5),
                sk("cx_ticket_management","Ticket management","Technical",3,1.5),
                sk("cx_sla_tracking","SLA tracking","Technical",2,1.0),
                sk("cx_customer_empathy","Customer empathy","Behavioural",3,2.0),
                sk("cx_conflict_resolution","Conflict resolution","Behavioural",2,1.5),
                sk("cx_written_communication","Written communication","Behavioural",3,1.5),
                sk("cx_isp_service","ISP service knowledge","Domain",2,1.5),
                sk("cx_broadband_basics","Broadband troubleshooting basics","Domain",2,1.0),
            ],
            "good_to_have_skills": [
                gth("cx_multilingual","Multilingual support","Behavioural",2,0.8),
                gth("cx_upsell","Upselling and retention","Domain",1,0.8),
            ]},
    }},
    "MKT": {"roles": {
        "marketing_manager": {"role_title": "Marketing Manager", "seniority": "Lead",
            "must_have_skills": [
                sk("mkt_digital_tools","Digital marketing (Meta/Google Ads)","Technical",3,2.0,True),
                sk("mkt_marketing_analytics","Marketing analytics","Technical",3,1.5,True),
                sk("mkt_content_management","Content management","Technical",3,1.0),
                sk("mkt_creative_thinking","Creative thinking","Behavioural",3,1.5),
                sk("mkt_brand_consistency","Brand consistency","Behavioural",3,1.5),
                sk("mkt_copywriting","Copywriting","Behavioural",3,1.0),
                sk("mkt_isp_market","ISP consumer market knowledge","Domain",3,1.5),
                sk("mkt_go_to_market","Go-to-market strategy","Strategic",3,2.0,True),
                sk("mkt_growth_marketing","Growth marketing strategy","Strategic",3,1.5,True),
            ],
            "good_to_have_skills": [
                gth("mkt_seo_sem","SEO/SEM","Technical",2,1.0),
                gth("mkt_brand_strategy","Brand strategy","Strategic",2,1.0),
            ]},
        "marketing_executive": {"role_title": "Marketing Executive", "seniority": "IC",
            "must_have_skills": [
                sk("mkt_digital_tools","Digital marketing (Meta/Google Ads)","Technical",2,2.0),
                sk("mkt_marketing_analytics","Marketing analytics","Technical",2,1.5),
                sk("mkt_content_management","Content management","Technical",3,1.0),
                sk("mkt_creative_thinking","Creative thinking","Behavioural",2,1.5),
                sk("mkt_brand_consistency","Brand consistency","Behavioural",3,1.5),
                sk("mkt_copywriting","Copywriting","Behavioural",2,1.0),
                sk("mkt_isp_market","ISP consumer market knowledge","Domain",2,1.5),
                sk("mkt_competitive_pos","Competitive positioning","Domain",2,1.5),
            ],
            "good_to_have_skills": [
                gth("mkt_seo_sem","SEO/SEM","Technical",2,1.0),
                gth("mkt_video_editing","Video editing","Technical",1,0.8),
            ]},
    }},
    "SUPPLY": {"roles": {
        "supply_manager": {"role_title": "Supply Manager", "seniority": "Lead",
            "must_have_skills": [
                sk("supply_procurement","Procurement systems","Technical",3,1.5),
                sk("supply_vendor_mgmt","Vendor management","Technical",3,2.0,True),
                sk("supply_inventory","Inventory control","Technical",3,1.5),
                sk("supply_negotiation","Negotiation skills","Behavioural",3,2.0,True),
                sk("supply_attention_detail","Attention to detail","Behavioural",3,1.5),
                sk("supply_telecom_hw","Telecom hardware knowledge","Domain",3,1.5),
                sk("supply_lco_chain","LCO supply chain","Domain",3,2.0,True),
                sk("supply_cost_optimization","Cost optimization strategy","Strategic",3,2.0,True),
                sk("supply_supplier_strategy","Supplier diversification strategy","Strategic",3,1.5),
            ],
            "good_to_have_skills": [
                gth("supply_erp","ERP systems","Technical",2,1.0),
                gth("supply_import_export","Import/export regulations","Domain",2,0.8),
            ]},
        "procurement_executive": {"role_title": "Procurement Executive", "seniority": "IC",
            "must_have_skills": [
                sk("supply_procurement","Procurement systems","Technical",2,1.5),
                sk("supply_vendor_mgmt","Vendor management","Technical",2,2.0),
                sk("supply_inventory","Inventory control","Technical",2,1.5),
                sk("supply_negotiation","Negotiation skills","Behavioural",2,2.0),
                sk("supply_attention_detail","Attention to detail","Behavioural",3,1.5),
                sk("supply_process_adherence","Process adherence","Behavioural",3,1.0),
                sk("supply_telecom_hw","Telecom hardware knowledge","Domain",2,1.5),
                sk("supply_lco_chain","LCO supply chain","Domain",2,2.0),
            ],
            "good_to_have_skills": [
                gth("supply_erp","ERP systems","Technical",2,1.0),
                gth("supply_supplier_rel","Supplier relationship management","Behavioural",2,1.0),
            ]},
    }},
    "HR": {"roles": {
        "hr_manager": {"role_title": "HR Manager", "seniority": "Lead",
            "must_have_skills": [
                sk("hr_hris","HRIS tools","Technical",3,1.5),
                sk("hr_payroll","Payroll systems","Technical",3,1.5),
                sk("hr_perf_tools","Performance management tools","Technical",3,1.0),
                sk("hr_empathy","Empathy and discretion","Behavioural",3,2.0,True),
                sk("hr_conflict_mediation","Conflict mediation","Behavioural",3,1.5),
                sk("hr_labour_law","Indian labour law","Domain",3,2.0),
                sk("hr_talent_market","Talent market knowledge","Domain",3,1.5),
                sk("hr_people_strategy","People strategy","Strategic",3,2.0,True),
                sk("hr_culture_building","Culture building","Strategic",3,1.5,True),
            ],
            "good_to_have_skills": [
                gth("hr_ats","ATS (applicant tracking)","Technical",2,1.0),
                gth("hr_org_design","Organizational design","Strategic",2,1.0),
            ]},
        "hr_executive": {"role_title": "HR Executive", "seniority": "IC",
            "must_have_skills": [
                sk("hr_hris","HRIS tools","Technical",2,1.5),
                sk("hr_payroll","Payroll systems","Technical",2,1.5),
                sk("hr_empathy","Empathy and discretion","Behavioural",3,2.0),
                sk("hr_communication","Communication and facilitation","Behavioural",3,1.5),
                sk("hr_labour_law","Indian labour law","Domain",2,2.0),
                sk("hr_compliance","HR compliance","Domain",3,1.5),
            ],
            "good_to_have_skills": [
                gth("hr_talent_market","Talent market knowledge","Domain",2,1.0),
                gth("hr_ats","ATS (applicant tracking)","Technical",2,0.8),
            ]},
    }},
    "ANALYTICS": {"roles": {
        "analytics_lead": {"role_title": "Analytics Lead", "seniority": "Lead",
            "must_have_skills": [
                sk("analytics_sql","SQL (advanced)","Technical",4,2.0,True),
                sk("analytics_python_r","Python / R for analysis","Technical",3,1.5),
                sk("analytics_bi_tools","BI tools (Tableau/Power BI/Metabase)","Technical",3,1.5,True),
                sk("analytics_problem_solving","Problem solving","Behavioural",3,1.5),
                sk("analytics_insight_comm","Communication of insights","Behavioural",3,2.0,True),
                sk("analytics_telecom_data","Telecom data analysis","Domain",3,2.0,True),
                sk("analytics_funnel","Funnel analytics","Domain",3,1.5),
                sk("analytics_data_strategy","Data strategy","Strategic",3,2.0,True),
                sk("analytics_roadmap","Analytics roadmap ownership","Strategic",3,1.5),
            ],
            "good_to_have_skills": [
                gth("analytics_ml","ML fundamentals","Technical",2,1.0),
                gth("analytics_pipeline","Data pipeline management","Technical",2,1.0),
            ]},
        "data_analyst": {"role_title": "Data Analyst", "seniority": "IC",
            "must_have_skills": [
                sk("analytics_sql","SQL (advanced)","Technical",3,2.0),
                sk("analytics_python_r","Python / R for analysis","Technical",2,1.5),
                sk("analytics_bi_tools","BI tools (Tableau/Power BI/Metabase)","Technical",2,1.5),
                sk("analytics_problem_solving","Problem solving","Behavioural",3,1.5),
                sk("analytics_insight_comm","Communication of insights","Behavioural",2,2.0),
                sk("analytics_attention_quality","Attention to data quality","Behavioural",3,1.5),
                sk("analytics_telecom_data","Telecom data analysis","Domain",2,2.0),
                sk("analytics_funnel","Funnel analytics","Domain",2,1.5),
            ],
            "good_to_have_skills": [
                gth("analytics_ml","ML fundamentals","Technical",1,1.0),
                gth("analytics_customer_behavior","Customer behavior modeling","Domain",2,1.0),
            ]},
    }},
    "SOL_DESIGN": {"roles": {
        "solution_architect": {"role_title": "Solution Architect", "seniority": "Lead",
            "must_have_skills": [
                sk("sol_network_design","Network architecture design","Technical",4,2.0,True),
                sk("sol_isp_infra","ISP infrastructure design","Technical",4,2.0,True),
                sk("sol_solution_costing","Solution costing","Technical",3,1.5),
                sk("sol_client_comm","Client communication","Behavioural",3,1.5),
                sk("sol_problem_solving","Technical problem solving","Behavioural",4,2.0),
                sk("sol_isp_solutions","ISP technical solutions","Domain",4,2.0,True),
                sk("sol_lco_integration","LCO integration knowledge","Domain",3,2.0),
                sk("sol_solution_strategy","Solution strategy","Strategic",3,1.5,True),
                sk("sol_pricing_models","Pricing models","Strategic",3,1.5),
            ],
            "good_to_have_skills": [
                gth("sol_technical_docs","Technical documentation","Technical",3,1.0),
                gth("sol_partnership_dev","Partnership development","Strategic",2,1.0),
            ]},
        "network_engineer": {"role_title": "Network Engineer", "seniority": "IC",
            "must_have_skills": [
                sk("sol_network_design","Network architecture design","Technical",3,2.0),
                sk("sol_isp_infra","ISP infrastructure design","Technical",3,2.0),
                sk("sol_solution_costing","Solution costing","Technical",2,1.5),
                sk("sol_technical_docs","Technical documentation","Technical",2,1.0),
                sk("sol_problem_solving","Technical problem solving","Behavioural",3,2.0),
                sk("sol_isp_solutions","ISP technical solutions","Domain",3,2.0),
                sk("sol_lco_integration","LCO integration knowledge","Domain",2,2.0),
                sk("sol_bandwidth_planning","Bandwidth planning","Domain",3,1.5),
            ],
            "good_to_have_skills": [
                gth("sol_client_comm","Client communication","Behavioural",2,1.0),
            ]},
    }},
    "USER_INS": {"roles": {
        "user_insights_lead": {"role_title": "User Insights Lead", "seniority": "Lead",
            "must_have_skills": [
                sk("ui_research_methods","User research methods","Technical",3,1.5),
                sk("ui_survey_design","Survey design","Technical",3,1.5,True),
                sk("ui_usability_testing","Usability testing","Technical",3,1.5),
                sk("ui_empathy","User empathy","Behavioural",3,2.0,True),
                sk("ui_analytical_thinking","Analytical thinking","Behavioural",3,1.5),
                sk("ui_isp_user_behavior","ISP user behavior patterns","Domain",3,2.0,True),
                sk("ui_research_strategy","Research strategy","Strategic",3,1.5,True),
                sk("ui_insight_to_action","Insight-to-action frameworks","Strategic",3,1.5),
            ],
            "good_to_have_skills": [
                gth("ui_data_tools","Data analysis tools","Technical",2,1.0),
                gth("ui_stakeholder_comm","Stakeholder communication","Behavioural",3,1.0),
            ]},
        "ux_researcher": {"role_title": "UX Researcher", "seniority": "IC",
            "must_have_skills": [
                sk("ui_research_methods","User research methods","Technical",2,1.5),
                sk("ui_survey_design","Survey design","Technical",2,1.5),
                sk("ui_usability_testing","Usability testing","Technical",2,1.5),
                sk("ui_empathy","User empathy","Behavioural",3,2.0),
                sk("ui_analytical_thinking","Analytical thinking","Behavioural",2,1.5),
                sk("ui_isp_user_behavior","ISP user behavior patterns","Domain",2,2.0),
            ],
            "good_to_have_skills": [
                gth("ui_data_tools","Data analysis tools","Technical",2,1.0),
            ]},
    }},
    "FOUNDERS": {"roles": {
        "strategy_associate": {"role_title": "Strategy Associate", "seniority": "IC",
            "must_have_skills": [
                sk("founders_biz_analysis","Business analysis","Technical",3,2.0,True),
                sk("founders_financial_modeling","Financial modeling","Technical",3,2.0,True),
                sk("founders_planning_tools","Strategic planning tools","Technical",3,1.5),
                sk("founders_exec_presence","Executive presence","Behavioural",3,1.5),
                sk("founders_cross_fn","Cross-functional influence","Behavioural",3,2.0,True),
                sk("founders_startup_ops","Startup operations","Domain",3,1.5),
                sk("founders_investor_rel","Investor relations basics","Domain",2,1.5),
                sk("founders_company_strategy","Company strategy alignment","Strategic",3,2.0,True),
                sk("founders_growth_strategy","Growth strategy","Strategic",3,2.0,True),
            ],
            "good_to_have_skills": [
                gth("founders_board_reporting","Board reporting","Technical",2,1.0),
                gth("founders_fundraising","Fundraising narrative","Strategic",2,1.0),
            ]},
    }},
    "LND": {"roles": {
        "lnd_manager": {"role_title": "L&D Manager", "seniority": "Lead",
            "must_have_skills": [
                sk("lnd_lms","LMS tools","Technical",3,1.5),
                sk("lnd_instructional_design","Instructional design","Technical",3,1.5,True),
                sk("lnd_needs_analysis","Training needs analysis","Technical",3,1.5),
                sk("lnd_facilitation","Facilitation skills","Behavioural",3,2.0,True),
                sk("lnd_adult_learning","Adult learning principles","Behavioural",3,1.5),
                sk("lnd_content_dev","Content development","Behavioural",3,1.0),
                sk("lnd_skills_taxonomy","Skill taxonomy design","Domain",3,1.5,True),
                sk("lnd_training_roi","Training ROI measurement","Domain",3,1.5),
                sk("lnd_strategy","L&D strategy","Strategic",3,2.0,True),
                sk("lnd_gap_priority","Skills gap prioritization","Strategic",3,2.0,True),
            ],
            "good_to_have_skills": [
                gth("lnd_learning_culture","Learning culture building","Strategic",2,1.0),
                gth("lnd_eval_tools","Assessment/evaluation tools","Technical",2,0.8),
            ]},
        "lnd_coordinator": {"role_title": "L&D Coordinator", "seniority": "IC",
            "must_have_skills": [
                sk("lnd_lms","LMS tools","Technical",2,1.5),
                sk("lnd_instructional_design","Instructional design","Technical",2,1.5),
                sk("lnd_needs_analysis","Training needs analysis","Technical",2,1.5),
                sk("lnd_facilitation","Facilitation skills","Behavioural",2,2.0),
                sk("lnd_adult_learning","Adult learning principles","Behavioural",2,1.5),
                sk("lnd_content_dev","Content development","Behavioural",2,1.0),
                sk("lnd_training_roi","Training ROI measurement","Domain",2,1.5),
            ],
            "good_to_have_skills": [
                gth("lnd_eval_tools","Assessment/evaluation tools","Technical",2,0.8),
            ]},
    }},
    "COMMS": {"roles": {
        "comms_manager": {"role_title": "Communications Manager", "seniority": "Lead",
            "must_have_skills": [
                sk("comms_pr_tools","PR and media tools","Technical",3,1.5),
                sk("comms_cms","Content management systems","Technical",3,1.0),
                sk("comms_social_media","Social media management","Technical",3,1.5,True),
                sk("comms_writing","Writing and editing","Behavioural",4,2.0,True),
                sk("comms_brand_voice","Brand voice consistency","Behavioural",3,1.5),
                sk("comms_media_relations","Media relations","Behavioural",3,1.5),
                sk("comms_isp_industry","ISP industry communications","Domain",3,1.5),
                sk("comms_strategy","Communications strategy","Strategic",3,2.0,True),
                sk("comms_brand_narrative","Brand narrative","Strategic",3,1.5,True),
            ],
            "good_to_have_skills": [
                gth("comms_crisis","Crisis communication","Domain",2,1.0),
                gth("comms_regulatory_pr","Regulatory PR","Domain",2,0.8),
            ]},
        "content_writer": {"role_title": "Content Writer", "seniority": "IC",
            "must_have_skills": [
                sk("comms_cms","Content management systems","Technical",2,1.0),
                sk("comms_social_media","Social media management","Technical",2,1.5),
                sk("comms_writing","Writing and editing","Behavioural",3,2.0),
                sk("comms_brand_voice","Brand voice consistency","Behavioural",3,1.5),
                sk("comms_isp_industry","ISP industry communications","Domain",2,1.5),
            ],
            "good_to_have_skills": [
                gth("comms_pr_tools","PR and media tools","Technical",2,1.0),
                gth("comms_crisis","Crisis communication","Domain",1,0.8),
            ]},
    }},
    "LABS": {"roles": {
        "labs_lead": {"role_title": "Labs Lead", "seniority": "Lead",
            "must_have_skills": [
                sk("labs_prototyping","Rapid prototyping","Technical",3,1.5),
                sk("labs_research_methods","Research methodology","Technical",3,1.5),
                sk("labs_tech_eval","Technology evaluation","Technical",3,2.0,True),
                sk("labs_innovation","Innovation mindset","Behavioural",3,2.0,True),
                sk("labs_hypothesis","Hypothesis-driven thinking","Behavioural",3,1.5),
                sk("labs_emerging_tech","Emerging ISP technology","Domain",3,2.0,True),
                sk("labs_product_innovation","Product innovation","Domain",3,1.5),
                sk("labs_innovation_strategy","Innovation strategy","Strategic",3,2.0,True),
                sk("labs_tech_roadmap","Technology roadmap","Strategic",3,1.5,True),
            ],
            "good_to_have_skills": [
                gth("labs_api","API integration","Technical",2,1.0),
                gth("labs_digital_transformation","Digital transformation","Strategic",2,1.0),
            ]},
        "labs_researcher": {"role_title": "Research Engineer", "seniority": "IC",
            "must_have_skills": [
                sk("labs_prototyping","Rapid prototyping","Technical",2,1.5),
                sk("labs_research_methods","Research methodology","Technical",3,1.5),
                sk("labs_tech_eval","Technology evaluation","Technical",2,2.0),
                sk("labs_innovation","Innovation mindset","Behavioural",3,2.0),
                sk("labs_hypothesis","Hypothesis-driven thinking","Behavioural",2,1.5),
                sk("labs_emerging_tech","Emerging ISP technology","Domain",2,2.0),
                sk("labs_product_innovation","Product innovation","Domain",2,1.5),
            ],
            "good_to_have_skills": [
                gth("labs_api","API integration","Technical",2,1.0),
            ]},
    }},
    "TECH_FUT": {"roles": {
        "tech_future_architect": {"role_title": "Future Tech Architect", "seniority": "Lead",
            "must_have_skills": [
                sk("techfut_cloud","Cloud architecture","Technical",4,2.0,True),
                sk("techfut_systems_design","Systems design","Technical",4,2.0),
                sk("techfut_devops","DevOps practices","Technical",3,1.5),
                sk("techfut_learning_agility","Learning agility","Behavioural",4,2.0,True),
                sk("techfut_systems_thinking","Systems thinking","Behavioural",3,1.5),
                sk("techfut_next_gen","Next-gen ISP technology (5G/fiber)","Domain",3,2.0,True),
                sk("techfut_digital_infra","Digital infrastructure","Domain",3,1.5),
                sk("techfut_tech_strategy","Technology strategy","Strategic",3,2.0,True),
                sk("techfut_future_proofing","Future-proofing architecture","Strategic",3,1.5,True),
            ],
            "good_to_have_skills": [
                gth("techfut_ai_ml","AI/ML fundamentals","Technical",2,1.0),
                gth("techfut_mentoring","Technical mentoring","Behavioural",3,1.0),
            ]},
        "cloud_engineer": {"role_title": "Cloud Engineer", "seniority": "IC",
            "must_have_skills": [
                sk("techfut_cloud","Cloud architecture","Technical",3,2.0),
                sk("techfut_systems_design","Systems design","Technical",3,2.0),
                sk("techfut_devops","DevOps practices","Technical",3,1.5),
                sk("techfut_learning_agility","Learning agility","Behavioural",3,2.0),
                sk("techfut_systems_thinking","Systems thinking","Behavioural",2,1.5),
                sk("techfut_next_gen","Next-gen ISP technology (5G/fiber)","Domain",2,2.0),
                sk("techfut_digital_infra","Digital infrastructure","Domain",2,1.5),
            ],
            "good_to_have_skills": [
                gth("techfut_ai_ml","AI/ML fundamentals","Technical",2,1.0),
            ]},
    }},
    "BIZ": {"roles": {
        "business_development_manager": {"role_title": "Business Development Manager", "seniority": "Lead",
            "must_have_skills": [
                sk("biz_crm","CRM systems","Technical",3,1.5),
                sk("biz_pitch_decks","Pitch deck development","Technical",3,1.5,True),
                sk("biz_negotiation","Negotiation","Behavioural",3,2.0,True),
                sk("biz_relationship","Relationship building","Behavioural",3,2.0,True),
                sk("biz_pitching","Pitching and presentation","Behavioural",3,1.5),
                sk("biz_isp_market","ISP market knowledge","Domain",3,1.5),
                sk("biz_partner_ecosystem","Partner/channel ecosystem","Domain",3,2.0,True),
                sk("biz_revenue_strategy","Revenue strategy","Strategic",3,2.0,True),
                sk("biz_market_expansion","Market expansion strategy","Strategic",3,1.5,True),
            ],
            "good_to_have_skills": [
                gth("biz_contract_mgmt","Contract management","Technical",2,1.0),
                gth("biz_partnership_strategy","Partnership strategy","Strategic",2,1.0),
            ]},
        "biz_dev_executive": {"role_title": "Business Development Executive", "seniority": "IC",
            "must_have_skills": [
                sk("biz_crm","CRM systems","Technical",2,1.5),
                sk("biz_pitch_decks","Pitch deck development","Technical",2,1.5),
                sk("biz_negotiation","Negotiation","Behavioural",2,2.0),
                sk("biz_relationship","Relationship building","Behavioural",3,2.0),
                sk("biz_pitching","Pitching and presentation","Behavioural",2,1.5),
                sk("biz_isp_market","ISP market knowledge","Domain",2,1.5),
                sk("biz_partner_ecosystem","Partner/channel ecosystem","Domain",2,2.0),
            ],
            "good_to_have_skills": [
                gth("biz_contract_mgmt","Contract management","Technical",2,1.0),
                gth("biz_revenue_models","Revenue models understanding","Domain",2,1.0),
            ]},
    }},
}

# ─── EMPLOYEES ────────────────────────────────────────────────────────────────
def emp(eid, name, role_title, fn, slug, manager, seniority):
    email = name.lower().replace(" ", ".").replace("dr.", "dr").replace("&", "and") + "@wiom.in"
    return {"employee_id": eid, "name": name, "role_title": role_title,
            "function_code": fn, "role_slug": slug, "manager": manager,
            "seniority": seniority, "email": email,
            "assessment_status": "submitted", "manager_rating_status": "submitted"}

ALL_EMPLOYEES = [
    # ── EXISTING functions (keep role slugs matching existing framework) ──────
    emp("EMP001","Rahul Sharma","Senior Backend Engineer","TECH","senior_backend_engineer","Pranav Chandra","Lead"),
    emp("EMP002","Priya Menon","Python Developer","TECH","python_developer","Rahul Sharma","IC"),
    emp("EMP003","Amit Kumar","Python Developer","TECH","python_developer","Rahul Sharma","IC"),
    emp("EMP004","Rohan Das","Mobile Lead","TECH","mobile_lead","Pranav Chandra","Lead"),
    emp("EMP005","Ravi Patel","Data Analyst","TECH","data_analyst","Rahul Sharma","IC"),
    emp("EMP006","Ananya Singh","Product Manager","PROD","product_manager","Pranav Chandra","IC"),
    emp("EMP007","Kavya Reddy","Senior Product Manager","PROD","senior_product_manager","Pranav Chandra","Lead"),
    emp("EMP008","Ankit Gupta","Product Manager","PROD","product_manager","Kavya Reddy","IC"),
    emp("EMP009","Sundar Krishnan","Director – Solution Design","PROD","director_solution_design","Pranav Chandra","Lead"),
    emp("EMP010","Meghna Pillai","Senior Product Manager","PROD","senior_product_manager","Pranav Chandra","Lead"),
    emp("EMP011","Pooja Iyer","Record to Report (R2R)","FIN","r2r_finance","Pranav Chandra","IC"),
    emp("EMP012","Aditya Nair","Record to Report (R2R)","FIN","r2r_finance","Pranav Chandra","IC"),
    # ── EXE ───────────────────────────────────────────────────────────────────
    emp("EMP013","Vikram Gupta","Execution Manager","EXE","execution_manager","Pranav Chandra","Lead"),
    emp("EMP014","Sana Khan","Execution Manager","EXE","execution_manager","Pranav Chandra","Lead"),
    emp("EMP015","Deepak Mehta","Operations Analyst","EXE","operations_analyst","Vikram Gupta","IC"),
    emp("EMP016","Rina Patel","Operations Analyst","EXE","operations_analyst","Vikram Gupta","IC"),
    emp("EMP017","Arun Mishra","Operations Analyst","EXE","operations_analyst","Sana Khan","IC"),
    # ── USER_INS ──────────────────────────────────────────────────────────────
    emp("EMP018","Neha Verma","User Insights Lead","USER_INS","user_insights_lead","Pranav Chandra","Lead"),
    emp("EMP019","Siddharth Roy","UX Researcher","USER_INS","ux_researcher","Neha Verma","IC"),
    # ── HR ────────────────────────────────────────────────────────────────────
    emp("EMP020","Meera Joshi","HR Manager","HR","hr_manager","Pranav Chandra","Lead"),
    emp("EMP021","Tanvi Singh","HR Executive","HR","hr_executive","Meera Joshi","IC"),
    emp("EMP022","Rohan Kapoor","HR Executive","HR","hr_executive","Meera Joshi","IC"),
    # ── LABS ──────────────────────────────────────────────────────────────────
    emp("EMP023","Dr. Kartik Nair","Labs Lead","LABS","labs_lead","Pranav Chandra","Lead"),
    emp("EMP024","Divya Sharma","Research Engineer","LABS","labs_researcher","Dr. Kartik Nair","IC"),
    # ── TECH_FUT ──────────────────────────────────────────────────────────────
    emp("EMP025","Sanjay Kumar","Future Tech Architect","TECH_FUT","tech_future_architect","Pranav Chandra","Lead"),
    emp("EMP026","Nikita Gupta","Cloud Engineer","TECH_FUT","cloud_engineer","Sanjay Kumar","IC"),
    emp("EMP027","Varun Singh","Cloud Engineer","TECH_FUT","cloud_engineer","Sanjay Kumar","IC"),
    # ── MKT ───────────────────────────────────────────────────────────────────
    emp("EMP028","Priyanka Desai","Marketing Manager","MKT","marketing_manager","Pranav Chandra","Lead"),
    emp("EMP029","Rahul Verma","Marketing Executive","MKT","marketing_executive","Priyanka Desai","IC"),
    emp("EMP030","Simran Gill","Marketing Executive","MKT","marketing_executive","Priyanka Desai","IC"),
    # ── CX ────────────────────────────────────────────────────────────────────
    emp("EMP031","Arvind Rao","CX Team Lead","CX","cx_team_lead","Pranav Chandra","Lead"),
    emp("EMP032","Kiran Bose","CX Team Lead","CX","cx_team_lead","Pranav Chandra","Lead"),
    emp("EMP033","Poornima Iyer","Customer Support Executive","CX","customer_support_exec","Arvind Rao","IC"),
    emp("EMP034","Rajan Pillai","Customer Support Executive","CX","customer_support_exec","Arvind Rao","IC"),
    emp("EMP035","Sunita Devi","Customer Support Executive","CX","customer_support_exec","Kiran Bose","IC"),
    # ── SUPPLY ────────────────────────────────────────────────────────────────
    emp("EMP036","Mahesh Agarwal","Supply Manager","SUPPLY","supply_manager","Pranav Chandra","Lead"),
    emp("EMP037","Tarun Saxena","Procurement Executive","SUPPLY","procurement_executive","Mahesh Agarwal","IC"),
    emp("EMP038","Gayatri Mishra","Procurement Executive","SUPPLY","procurement_executive","Mahesh Agarwal","IC"),
    emp("EMP039","Nikhil Yadav","Procurement Executive","SUPPLY","procurement_executive","Mahesh Agarwal","IC"),
    # ── FOUNDERS ──────────────────────────────────────────────────────────────
    emp("EMP040","Shreya Kapoor","Strategy Associate","FOUNDERS","strategy_associate","Pranav Chandra","IC"),
    emp("EMP041","Abhijeet Das","Strategy Associate","FOUNDERS","strategy_associate","Pranav Chandra","IC"),
    # ── SOL_DESIGN ────────────────────────────────────────────────────────────
    emp("EMP042","Gopal Nair","Solution Architect","SOL_DESIGN","solution_architect","Pranav Chandra","Lead"),
    emp("EMP043","Leena Joshi","Network Engineer","SOL_DESIGN","network_engineer","Gopal Nair","IC"),
    emp("EMP044","Vinay Kumar","Network Engineer","SOL_DESIGN","network_engineer","Gopal Nair","IC"),
    # ── ANALYTICS ─────────────────────────────────────────────────────────────
    emp("EMP045","Ranjit Sharma","Analytics Lead","ANALYTICS","analytics_lead","Pranav Chandra","Lead"),
    emp("EMP046","Priya Khatri","Data Analyst","ANALYTICS","data_analyst","Ranjit Sharma","IC"),
    emp("EMP047","Dev Menon","Data Analyst","ANALYTICS","data_analyst","Ranjit Sharma","IC"),
    # ── COMMS ─────────────────────────────────────────────────────────────────
    emp("EMP048","Kavita Reddy","Communications Manager","COMMS","comms_manager","Pranav Chandra","Lead"),
    emp("EMP049","Anand Bhat","Content Writer","COMMS","content_writer","Kavita Reddy","IC"),
    # ── LND ───────────────────────────────────────────────────────────────────
    emp("EMP050","Shilpa Mohan","L&D Manager","LND","lnd_manager","Pranav Chandra","Lead"),
    emp("EMP051","Jitendra Pal","L&D Coordinator","LND","lnd_coordinator","Shilpa Mohan","IC"),
    # ── BIZ ───────────────────────────────────────────────────────────────────
    emp("EMP052","Rajesh Srivastava","Business Development Manager","BIZ","business_development_manager","Pranav Chandra","Lead"),
    emp("EMP053","Naina Singh","Business Development Executive","BIZ","biz_dev_executive","Rajesh Srivastava","IC"),
]

# ─── ASSESSMENT GENERATION ───────────────────────────────────────────────────
def get_all_skills_for_role(framework, fn_code, role_slug):
    """Return flat list of all skills (must_have + good_to_have) for a role."""
    role = framework.get("functions", {}).get(fn_code, {}).get("roles", {}).get(role_slug, {})
    return role.get("must_have_skills", []) + role.get("good_to_have_skills", [])

def gen_self_rating(expected_level, seniority):
    """Realistic self-rating: Leads tend to rate 0-1 below expected, ICs 1-2 below."""
    if seniority == "Lead":
        gap = random.choices([0, 1, 1, 2], weights=[25, 40, 25, 10])[0]
    else:
        gap = random.choices([0, 1, 1, 2, 2, 3], weights=[10, 25, 30, 20, 10, 5])[0]
    return max(1, min(4, expected_level - gap))

def gen_mgr_rating(self_rating, expected_level):
    """Manager ratings: usually within ±1 of self, slightly conservative."""
    delta = random.choices([-1, 0, 0, 0, 1], weights=[15, 40, 30, 10, 5])[0]
    return max(1, min(4, self_rating + delta))

def gen_growth_potential(seniority):
    """Manager's assessment of growth potential. Lead roles skewed High/Med, ICs more spread."""
    if seniority == "Lead":
        return random.choices(["High", "Medium", "Low"], weights=[50, 35, 15])[0]
    else:
        return random.choices(["High", "Medium", "Low"], weights=[20, 55, 25])[0]

def make_assessment(employee, framework):
    eid = employee["employee_id"]
    fn = employee["function_code"]
    slug = employee["role_slug"]
    seniority = employee["seniority"]
    skills = get_all_skills_for_role(framework, fn, slug)
    if not skills:
        return None

    ratings = []
    for s in skills:
        r = gen_self_rating(s["expected_level"], seniority)
        ratings.append({
            "skill_id": s["skill_id"], "skill_name": s["skill_name"],
            "self_rating": r, "confidence": random.choice(["high","medium","medium","low"])
        })
    return {
        "employee_id": eid, "function_code": fn,
        "role_title": employee["role_title"],
        "ratings": ratings,
        "submitted_at": ts(random.randint(0, 18))
    }

def make_mgr_rating(employee, assessment, framework):
    if not assessment:
        return None
    fn = employee["function_code"]
    slug = employee["role_slug"]
    expected_map = {s["skill_id"]: s["expected_level"]
                    for s in get_all_skills_for_role(framework, fn, slug)}
    ratings = []
    for r in assessment["ratings"]:
        exp = expected_map.get(r["skill_id"], r["self_rating"])
        mgr = gen_mgr_rating(r["self_rating"], exp)
        ratings.append({
            "skill_id": r["skill_id"], "skill_name": r["skill_name"],
            "self_rating": mgr
        })
    return {
        "manager_id": employee["manager"],
        "employee_id": employee["employee_id"],
        "ratings": ratings,
        "coaching_notes": "",
        "growth_potential": gen_growth_potential(employee["seniority"]),
        "submitted_at": ts(random.randint(0, 10))
    }

# ─── MAIN ────────────────────────────────────────────────────────────────────
def main():
    # 1. Load existing framework and add new functions
    fw_path = DATA_DIR / "skill_framework.json"
    if fw_path.exists():
        with open(fw_path, encoding="utf-8") as f:
            framework = json.load(f)
    else:
        framework = {"_meta": {"last_updated": ""}, "functions": {}}

    # Add Strategic skills to existing PROD manager roles (fills Strategic column)
    prod_roles = framework.get("functions", {}).get("PROD", {}).get("roles", {})
    strategic_prod = [
        sk("prod_product_strategy","Product strategy & vision","Strategic",3,2.0,True),
        sk("prod_okr_ownership","OKR ownership","Strategic",3,1.5,True),
    ]
    for role_slug, role_data in prod_roles.items():
        if role_data.get("seniority") in ("Lead",):
            existing_ids = {s["skill_id"] for s in role_data.get("must_have_skills",[])}
            for s in strategic_prod:
                if s["skill_id"] not in existing_ids:
                    role_data.setdefault("must_have_skills",[]).append(s)

    # Add Strategic skills to TECH manager roles
    tech_roles = framework.get("functions", {}).get("TECH", {}).get("roles", {})
    strategic_tech = [
        sk("tech_engineering_strategy","Engineering roadmap & strategy","Strategic",3,2.0,True),
        sk("tech_team_growth","Team capability building","Strategic",3,1.5,True),
    ]
    for role_slug, role_data in tech_roles.items():
        if role_data.get("seniority") in ("Lead",):
            existing_ids = {s["skill_id"] for s in role_data.get("must_have_skills",[])}
            for s in strategic_tech:
                if s["skill_id"] not in existing_ids:
                    role_data.setdefault("must_have_skills",[]).append(s)

    # Add new functions
    for fn_code, fn_data in NEW_FUNCTIONS.items():
        framework["functions"][fn_code] = fn_data

    framework["_meta"]["last_updated"] = ts()

    with open(fw_path, "w", encoding="utf-8") as f:
        json.dump(framework, f, indent=2, ensure_ascii=False)
    print(f"OK skill_framework.json — {len(framework['functions'])} functions")

    # 2. Write employees
    emp_path = DATA_DIR / "employees.json"
    with open(emp_path, "w", encoding="utf-8") as f:
        json.dump({"employees": ALL_EMPLOYEES}, f, indent=2, ensure_ascii=False)
    print(f"OK employees.json — {len(ALL_EMPLOYEES)} employees")

    # 3. Generate assessments
    assessments = []
    mgr_ratings = []
    assess_map = {}  # employee_id -> assessment

    for e in ALL_EMPLOYEES:
        a = make_assessment(e, framework)
        if a:
            assessments.append(a)
            assess_map[e["employee_id"]] = a

    # 4. Generate manager ratings (for employees whose manager has an assessment too)
    for e in ALL_EMPLOYEES:
        a = assess_map.get(e["employee_id"])
        if a:
            mr = make_mgr_rating(e, a, framework)
            if mr:
                mgr_ratings.append(mr)

    with open(DATA_DIR / "assessments.json", "w", encoding="utf-8") as f:
        json.dump({"assessments": assessments}, f, indent=2, ensure_ascii=False)
    print(f"OK assessments.json — {len(assessments)} entries")

    with open(DATA_DIR / "manager_ratings.json", "w", encoding="utf-8") as f:
        json.dump({"ratings": mgr_ratings}, f, indent=2, ensure_ascii=False)
    print(f"OK manager_ratings.json — {len(mgr_ratings)} entries")

    # 5. org_structure (summary only)
    org = {
        "_meta": {"description": "Wiom org structure", "last_updated": ts(), "total_headcount": len(ALL_EMPLOYEES)},
        "functions": [
            {"code": fn, "name": fn, "headcount": sum(1 for e in ALL_EMPLOYEES if e["function_code"] == fn),
             "managers": sum(1 for e in ALL_EMPLOYEES if e["function_code"] == fn and e["seniority"] == "Lead")}
            for fn in dict.fromkeys(e["function_code"] for e in ALL_EMPLOYEES)
        ]
    }
    with open(DATA_DIR / "org_structure.json", "w", encoding="utf-8") as f:
        json.dump(org, f, indent=2, ensure_ascii=False)
    print(f"OK org_structure.json — {len(org['functions'])} functions")

    print(f"\nDone. {len(ALL_EMPLOYEES)} employees, {len(assessments)} assessments, {len(mgr_ratings)} manager ratings")
    print("Run: curl -X POST <railway-url>/api/v1/admin/seed -H 'X-Admin-Key: Wiom@1234'")

if __name__ == "__main__":
    main()
