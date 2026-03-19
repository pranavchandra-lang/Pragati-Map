# Wiom Talent Intelligence Platform — Claude Code Project

## What this project is
An AI-powered org skill mapping and personalised upskilling system for Wiom, an early-stage ISP operating through LCO partner networks in India. Built from zero — no existing skill maps, learning plans, or HR systems.

## Business objective
Map the full organisational skill landscape and generate personalised upskilling paths for every employee, anchored to Wiom's strategic priorities.

## Current state (what exists)
- Functional team structure: function names, team sizes, manager counts, IC counts
- JD skill extraction complete: must-have and good-to-have skills per critical role (JSON + Google Sheet)
- Phase 1 agent (JD extraction) built as HTML artifact — working

## What we are building next
Full-stack web application deployable on Railway:
- Backend: Python FastAPI
- Frontend: Plain HTML/CSS/JS (no build step)
- Storage: JSON flat files → upgradeable to SQLite
- AI layer: Claude API (claude-sonnet-4-5-20251001) for reasoning, gap analysis, path generation

## Architecture
```
wiom-talent/
├── CLAUDE.md                  ← this file
├── README.md
├── Procfile                   ← Railway deployment
├── requirements.txt
├── .env.example
├── data/
│   ├── org_structure.json     ← team structure, sizes, managers, ICs
│   ├── skill_framework.json   ← extracted skills per function (from JD agent output)
│   ├── assessments.json       ← employee self-assessments (grows over time)
│   ├── manager_ratings.json   ← manager assessments of direct reports
│   └── employees.json         ← employee roster (name, role, function, manager)
├── backend/
│   ├── main.py                ← FastAPI app entry point
│   ├── routers/
│   │   ├── bootstrap.py       ← POST /bootstrap — seed org + framework from JSON
│   │   ├── assessment.py      ← GET/POST /assess — employee self-assessment form
│   │   ├── manager.py         ← GET/POST /manager — manager rating endpoints
│   │   ├── admin.py           ← GET /admin/* — heatmap, gaps, framework editor
│   │   └── ai.py              ← POST /ai/* — Claude-powered analysis endpoints
│   ├── services/
│   │   ├── skill_engine.py    ← gap scoring, delta calculation, 9-box overlay
│   │   ├── path_engine.py     ← 70-20-10 upskilling path generation
│   │   └── claude_client.py   ← Anthropic API wrapper
│   └── models/
│       └── schemas.py         ← Pydantic models
├── frontend/
│   ├── index.html             ← landing / employee entry point
│   ├── assess.html            ← employee self-assessment form
│   ├── manager.html           ← manager rating form
│   └── admin/
│       ├── dashboard.html     ← org heatmap, gap reports
│       ├── framework.html     ← skill framework editor
│       └── employee.html      ← individual employee deep-dive
└── scripts/
    ├── import_jd_skills.py    ← converts JD agent JSON output → skill_framework.json
    └── import_org_structure.py ← converts your team structure data → org_structure.json

```

## Key design decisions (locked)
1. **Triangulated data model** — skill score = weighted avg of self (40%) + manager (50%) + peer (10%)
2. **Skill taxonomy structure** — 4 tiers: Core (all Wiom), Function, Role, Emerging
3. **Gap-to-intervention via 70-20-10** — Claude recommends experiences (stretch assignments, mentors) NOT just courses
4. **9-box overlay** — performance × skill-readiness grid on admin dashboard
5. **Employee-facing output** — employees see their own skill map and growth plan (not HR-only)
6. **Living framework** — skill pools have a `last_reviewed` date and trigger review alerts at 90 days

## Skill levels (universal scale)
- 1 = Awareness — knows the concept, cannot apply independently
- 2 = Working — applies with guidance, needs support
- 3 = Practitioner — applies independently, reliable
- 4 = Expert — teaches others, sets standards

## Skill taxonomy categories
- Technical — tools, systems, domain-specific hard skills
- Behavioural — communication, leadership, collaboration, mindset
- Domain — ISP/telecom industry knowledge, regulatory, customer
- Strategic — OKR thinking, business acumen, cross-functional influence

## Gap scoring logic
```
expected_level  = skill_framework[function][role][skill].expected_level
actual_level    = triangulated_score(self, manager, peer)
gap_score       = expected_level - actual_level
priority        = gap_score × skill_framework[skill].business_criticality_weight
```

## 70-20-10 path generation rules (for Claude prompts)
- Gap ≥ 2 levels → must include a stretch assignment recommendation
- Gap = 1 level → social learning first (mentor pairing), formal second
- Gap < 1 → maintenance — suggest peer teaching opportunity (reinforces mastery)
- Always surface internal experts: employees at level 3-4 in that skill who can mentor

## Claude API usage pattern
- Model: claude-sonnet-4-5-20251001
- Use for: gap narrative, path generation, framework suggestions, heatmap insights
- Do NOT use for: data storage, CRUD operations, form validation
- Always structured JSON output with try/catch and brace-extraction fallback

## Data inputs available NOW
1. Functional team structure (to be imported via import_org_structure.py)
2. JD skill extraction JSON (to be imported via import_jd_skills.py)

## What to build in order
1. `scripts/import_org_structure.py` — paste your team structure, get org_structure.json
2. `scripts/import_jd_skills.py` — takes JD agent JSON output, normalises into skill_framework.json
3. `backend/main.py` + basic FastAPI skeleton
4. `frontend/assess.html` — employee self-assessment (most urgent user-facing surface)
5. `backend/services/skill_engine.py` — gap scoring
6. `backend/services/path_engine.py` — 70-20-10 recommendations
7. `frontend/admin/dashboard.html` — heatmap and gap reports
8. Railway deployment

## Environment variables
```
ANTHROPIC_API_KEY=sk-...
ADMIN_PASSWORD=changeme
DATA_DIR=./data
PORT=8000
```

## Wiom domain context (always keep in mind)
- Functions: Product, Tech, Ops, Growth, Finance, HR, Strategy (confirm list with Pranav)
- ISP operating through LCO (Local Cable Operator) partner networks
- Fast-moving, early-stage — skill framework must be lightweight and maintainable by 1 HRBP
- Many employees may be semi-technical — UX of assessment form must be dead simple
- Manager buy-in is a prerequisite — manager rating form ships before employee form goes live

## Change management hooks (baked into the product)
- Employee assessment form opens with a 3-line "why this matters to you" message
- Employees always receive their own skill report after submitting
- Manager dashboard shows coaching conversation starters per direct report
- Framework has a `strategic_priority` boolean per skill — anchors map to business direction

## Conventions
- All JSON keys: snake_case
- Skill IDs: `{function_code}_{skill_slug}` e.g. `ops_network_troubleshooting`
- API routes: `/api/v1/...`
- Frontend: no frameworks, vanilla JS only, dark theme matching JD agent aesthetic
