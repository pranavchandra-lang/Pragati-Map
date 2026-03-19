# Pragati Map — Release Note
### Wiom Talent Intelligence Platform · v1.0 · March 2026

---

## Executive Summary

Pragati Map is Wiom's first internal talent intelligence system. It gives every employee a personalised skill map and AI-generated growth plan, gives managers visibility into their team's readiness gaps, and gives the People team an org-wide skill heatmap with strategic AI insights — all from a single web application, deployed on Wiom's Railway infrastructure, accessible on any device.

---

## The Problem We Solved

Wiom is scaling fast. As of early 2026, we have no formal skill mapping, no learning plans tied to business priorities, and no way for HR to answer: *"Where are our biggest capability gaps, and what do we do about them?"*

The existing approach:
- Skill gaps identified reactively (after projects fail or people leave)
- L&D spend not anchored to strategic priorities
- Managers lack structured tools for coaching conversations
- No employee-facing growth visibility → low retention signal

We needed a system that could be deployed in days, not months, work with the team we have now (not after a 6-month data-collection exercise), and give every person at Wiom a reason to use it.

---

## What We Built

A full-stack web application with three user-facing surfaces and an AI reasoning layer.

### User Surfaces

| Surface | Who Uses It | What They Do |
|---------|------------|--------------|
| **Employee Assessment** (`/assess.html`) | Every Wiom employee | 3-minute self-assessment → instant personal skill map + top 3 growth priorities |
| **Manager Rating** (`/manager.html`) | Team managers | Rate each direct report's skills alongside their self-assessment, add coaching notes |
| **People Team Dashboard** (`/admin/dashboard.html`) | HRBP, leadership | Org heatmap, function-level breakdowns, 9-box talent grid, AI strategic insights |

---

## Features and Their Rationale

### 1. Triangulated Skill Scoring
**What it does:** Each skill score is a weighted average of self-assessment (44%) and manager rating (56%). Peer ratings are structurally supported but not yet collected.

**Why this approach:** Single-source ratings are unreliable. Self-ratings skew high; manager ratings alone miss employee context. Triangulation gives a more honest signal. The 44/56 split slightly weights the manager to reduce self-inflation while not discarding employee voice.

---

### 2. Universal 4-Level Skill Scale
Every skill is rated on the same scale across all roles and functions:

| Level | Label | Meaning |
|-------|-------|---------|
| 1 | Awareness | Knows the concept, cannot apply independently |
| 2 | Working | Applies with guidance, needs support |
| 3 | Practitioner | Applies independently, reliably |
| 4 | Expert | Teaches others, sets standards |

**Why this approach:** A common scale allows cross-function comparison and makes assessments comparable over time. It avoids jargon and is simple enough for non-HR employees to self-rate honestly.

---

### 3. Role-Specific Skill Framework (JD-Derived)
**What it does:** Skills are pulled directly from real Wiom job descriptions — not a generic competency library. Each skill has:
- `expected_level` (what the role requires)
- `business_criticality_weight` (1.0–2.0 multiplier for priority scoring)
- `strategic_priority` flag
- `must_have` vs. `good_to_have` classification

**Current coverage:** 9 roles across Product (PROD), Tech (TECH), and Finance (FIN) functions. 146 skills total (84 must-have, 62 good-to-have).

**Why this approach:** Generic competency frameworks don't map to Wiom's actual work. Starting from JDs ensures every skill in the system is one Wiom actively hires for and needs.

---

### 4. Gap Scoring Engine
**Formula:**
```
gap_score     = expected_level − triangulated_score
priority_score = gap_score × business_criticality_weight
```

Skills are ranked by priority score. A gap of 0 or below is marked "met" or "exceeds". The top gaps drive the AI growth plan.

**Why this approach:** Not all gaps are equal. A gap in a business-critical skill (weight 2.0) is twice as urgent as a gap in a supporting skill (weight 1.0). This ensures resources go to the right places first.

---

### 5. AI-Generated 70-20-10 Growth Plans
**What it does:** For each employee, the AI (Gemini 2.5 Flash Lite) generates a personalised upskilling path for their top 3 priority gaps. Each recommendation follows the 70-20-10 framework:
- **70% Experiential** — stretch assignments, on-the-job practice
- **20% Social** — mentoring, shadowing, peer learning
- **10% Formal** — courses, certifications, structured training

**Gap-size logic:**
- Gap ≥ 2 levels → must include a stretch assignment
- Gap = 1 level → social learning first (mentoring), formal second
- Gap < 1 → maintenance — suggest a peer teaching opportunity to reinforce mastery

**Why this approach:** Most L&D spend in India goes on courses that don't change behaviour. 70-20-10 ensures the growth plan is anchored in real work, not just learning hours. AI generation makes it scalable to every employee without HR bandwidth.

---

### 6. Org-Level Skill Heatmap
**What it does:** A matrix showing average gap scores by function × skill category (Technical, Behavioural, Domain, Strategic). Colour-coded: green (gap 0), amber (gap 1), red (gap ≥ 2).

**Why this approach:** Gives HRBP and leadership a single-screen answer to "where are we collectively weak?" without reading individual reports.

---

### 7. Function-Level Heatmap with Employee Cards
**What it does:** Tabs per function (TECH, PROD, FIN) showing each employee's top 3 gaps with colour-coded severity bars. Pending (unassessed) employees are listed separately.

**Why this approach:** The org heatmap shows averages; the function view shows individuals. Managers and HRBPs need both levels to act.

---

### 8. 9-Box Talent Grid
**What it does:** A 3×3 grid plotting employees on:
- **X-axis** — Skill Readiness (inverted average gap score: low gap = high readiness)
- **Y-axis** — Performance Proxy (seniority: Junior / Mid / Senior)

Cells are labelled: Star, High Potential, Core Player, Rising Talent, Solid Performer, Needs Development, etc.

**Why this approach:** The 9-box is a standard HR prioritisation tool. In the absence of formal performance review data, seniority is a reasonable proxy for performance tier. The grid makes talent distribution visible at a glance and triggers the right conversations about investment vs. risk.

---

### 9. AI Heatmap Insights
**What it does:** A single button on the admin dashboard sends the full skill gap matrix to the AI and returns 3 strategic insights:
- `biggest_gap` — most critical collective skill gap
- `emerging_risk` — a risk that will grow if unaddressed
- `strategic_recommendation` — one actionable recommendation tied to business growth

**Why this approach:** Raw numbers don't tell a story. The AI layer transforms the heatmap into language that a leadership team can act on — without requiring the HRBP to interpret the data manually.

---

## Technical Architecture

```
Wiom Talent Intelligence Platform
├── Backend: Python FastAPI (uvicorn, Railway)
├── Frontend: Vanilla HTML/CSS/JS (no build step, dark theme)
├── Storage: Flat JSON files on Railway Volume (DATA_DIR=/data)
│   ├── employees.json        — roster with role slugs, seniority, manager
│   ├── skill_framework.json  — JD-derived skills by function × role
│   ├── assessments.json      — employee self-assessments
│   ├── manager_ratings.json  — manager assessments of direct reports
│   └── data/paths/           — cached AI-generated growth plans per employee
├── AI: Google Gemini 2.5 Flash Lite via direct REST API (v1)
│   └── Function kept as call_claude() for import compatibility
└── Auth: Admin — session cookie OR X-Admin-Key header
         Employees/Managers — open (SSO planned, not in v1)
```

### Key API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/v1/assess/{employee_id}` | Load skill form for employee |
| POST | `/api/v1/assess` | Submit self-assessment |
| GET | `/api/v1/manager/directs/{manager_name}` | Load direct reports |
| POST | `/api/v1/manager/rate` | Submit manager rating |
| GET | `/api/v1/admin/heatmap` | Org gap matrix |
| GET | `/api/v1/admin/gaps/{employee_id}` | Individual gap report |
| POST | `/api/v1/ai/path` | Generate AI growth plan |
| POST | `/api/v1/ai/heatmap-insights` | Generate AI strategic insights |
| POST | `/api/v1/admin/seed` | Copy repo data → Railway volume |

---

## Concepts Used

| Concept | Application |
|---------|------------|
| **70-20-10 Learning Model** | Growth plan structure for every employee |
| **Triangulated Assessment** | Self + manager weighted scoring to reduce bias |
| **9-Box Talent Grid** | Performance × readiness matrix for talent prioritisation |
| **Business Criticality Weighting** | Gap × weight = priority score (ensures strategic alignment) |
| **JD-Anchored Skill Framework** | Skills derived from real JDs, not generic competency libraries |
| **Retrieval-Augmented Generation (RAG-lite)** | Skill gap data passed as context to the AI before generating plans |
| **70% Cache-First AI** | Growth plans cached per employee to reduce API costs and latency |
| **F-Pattern Layout** | Critical information top-left, scannable visual hierarchy (WIOM design system) |
| **Hindi-First UX** | All employee-facing copy in Hindi (Devanagari) to reduce friction for non-English-primary users |

---

## Known Limitations (v1)

| Limitation | Impact | Planned Fix |
|-----------|--------|------------|
| **No peer ratings** | Triangulation is self + manager only (44/56 split). Intended 40/50/10 | Collect peer data in v1.1 |
| **No employee authentication** | Any user can access any employee's assessment form by ID | Google OAuth (`@wiom.in` + `@i2e1.com`) — design complete, not deployed |
| **Flat file storage** | JSON files have no transactions; concurrent writes use a threading lock but are not ACID | Migrate to SQLite or Postgres in v2 |
| **Stale path cache** | AI growth plans are cached indefinitely; don't reflect new manager ratings | Add cache TTL or clear-cache endpoint per employee |
| **Framework coverage** | Only PROD, TECH, FIN functions mapped. OPS, GROWTH, HR, Strategy not yet in framework | HRBP to run JD extraction agent for remaining functions |
| **Seniority as performance proxy** | 9-box Y-axis uses seniority level, not actual performance ratings | Wire to performance review data when available |
| **AI quota (free tier)** | Gemini 2.5 Flash Lite on AI Studio free tier has rate limits; heavy concurrent use may hit 429 | Upgrade to paid tier or add retry/backoff logic |
| **No audit log** | No record of who submitted what, when | Add timestamped submission logs in v1.1 |

---

## Deployment

- **Platform:** Railway (Wiom account)
- **Live URL:** `https://web-production-d17e6.up.railway.app`
- **Data persistence:** Railway Volume mounted at `/data` (`DATA_DIR=/data`)
- **Process:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- **Seed data:** `POST /api/v1/admin/seed` with `X-Admin-Key` header — copies committed JSON data to volume on first deploy

### Environment Variables Required

| Variable | Purpose |
|---------|---------|
| `GEMINI_API_KEY` | Google AI Studio API key (free tier, Gemini 2.5 Flash Lite) |
| `ADMIN_PASSWORD` | Admin dashboard password (also accepted as `X-Admin-Key` header) |
| `DATA_DIR` | Path to persistent data volume (Railway: `/data`) |
| `SESSION_SECRET` | Signed cookie secret for admin sessions |
| `PORT` | Injected by Railway automatically |

---

## What's Next (Backlog)

1. **Google OAuth** — restrict access to `@wiom.in` and `@i2e1.com` accounts
2. **OPS, GROWTH, HR, Strategy frameworks** — run JD extraction agent on remaining functions
3. **Peer ratings** — add a lightweight peer nomination flow to complete the triangulation
4. **Manager coaching prompts** — surface AI-generated conversation starters on the manager dashboard
5. **Framework editor** — allow HRBP to update `expected_level` and `business_criticality_weight` per skill without editing JSON
6. **SQLite migration** — replace flat files with a proper database for concurrent access safety
7. **Mobile responsiveness** — current design is desktop-first; employee assessment form needs responsive treatment for field staff

---

*Built for Wiom's internal People & Culture hackathon, March 2026.*
*Authored by Pranav Chandra · Powered by Google Gemini 2.5 Flash Lite*
