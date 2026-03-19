"""
Pydantic schemas — all request/response contracts
"""
from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel


# ── Employee ──────────────────────────────────────────────────────────────────

class Employee(BaseModel):
    employee_id: str
    name: str
    role_title: str
    function_code: str
    manager: str
    seniority: str
    assessment_status: str
    manager_rating_status: str


# ── Skill ratings ─────────────────────────────────────────────────────────────

class SkillRating(BaseModel):
    skill_id: str
    skill_name: str
    self_rating: int  # 1–4
    confidence: Optional[str] = None  # "low" | "medium" | "high"


class AssessmentSubmit(BaseModel):
    employee_id: str
    function_code: str
    role_title: str
    ratings: List[SkillRating]
    submitted_at: Optional[str] = None


class ManagerRatingSubmit(BaseModel):
    manager_id: str
    employee_id: str
    ratings: List[SkillRating]
    coaching_notes: Optional[str] = None
    submitted_at: Optional[str] = None


# ── Gap analysis ──────────────────────────────────────────────────────────────

class GapResult(BaseModel):
    skill_id: str
    skill_name: str
    category: str
    type: str
    self_score: float
    manager_score: float
    triangulated_score: float
    expected_level: float
    gap_score: float
    priority_score: float
    status: Literal["gap", "met", "exceeds"]


# ── AI upskilling path ────────────────────────────────────────────────────────

class Intervention(BaseModel):
    experiential_70: str
    social_20: str
    formal_10: str


class SkillPriority(BaseModel):
    skill_name: str
    gap_score: float
    interventions: Intervention
    timeline_weeks: int
    success_indicator: str


class UpskillingPath(BaseModel):
    employee_id: str
    employee_name: str
    top_3_priorities: List[SkillPriority]
    quick_wins: List[str]
    manager_coaching_prompts: List[str]


class PathRequest(BaseModel):
    employee_id: str
    employee_name: str
    function_context: str


# ── Bootstrap ─────────────────────────────────────────────────────────────────

class BootstrapResponse(BaseModel):
    status: str
    functions_loaded: int
    roles_loaded: int
    employees_loaded: int


# ── Heatmap ───────────────────────────────────────────────────────────────────

class HeatmapWorstGap(BaseModel):
    function: str
    skill: str
    avg_gap: float


class HeatmapResponse(BaseModel):
    functions: List[str]
    categories: List[str]
    matrix: dict
    worst_gaps: List[HeatmapWorstGap]
    assessed_count: int
    total_count: int


# ── Auth / session ────────────────────────────────────────────────────────────

class UserSession(BaseModel):
    email: str
    name: str
    role: Literal["admin", "employee"]
    picture: Optional[str] = None
