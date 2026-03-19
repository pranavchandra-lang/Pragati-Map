# Wiom Talent Intelligence Platform

AI-powered org skill mapping and personalised upskilling — built for Wiom's people function.

## Quickstart

```bash
# 1. Clone and setup
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# → Add your ANTHROPIC_API_KEY to .env

# 2. Seed your org data
# Edit scripts/import_org_structure.py → fill in ORG_DATA dict
python scripts/import_org_structure.py

# 3. Import JD skill extraction output
python scripts/import_jd_skills.py --input path/to/jd_agent_output.json

# 4. Run the server
uvicorn backend.main:app --reload

# → Open http://localhost:8000
```

## Data flow

```
JD Agent JSON ──► import_jd_skills.py ──► skill_framework.json
Org structure ──► import_org_structure.py ──► org_structure.json + employees.json

Employee opens assess.html → submits ratings → assessments.json
Manager opens manager.html → rates direct reports → manager_ratings.json

skill_engine.py → triangulates scores → gap list per employee
path_engine.py + Claude → generates 70-20-10 upskilling plan
admin dashboard → org heatmap, gap reports, 9-box overlay
```

## Key files to edit first

| File | What to do |
|------|------------|
| `scripts/import_org_structure.py` | Fill in `ORG_DATA` with your real team structure |
| `scripts/import_jd_skills.py` | Run with `--input` pointing to JD agent JSON |
| `.env` | Add `ANTHROPIC_API_KEY` |

## Deploy to Railway

1. Push to GitHub
2. New Railway project → Deploy from GitHub repo
3. Add environment variables (ANTHROPIC_API_KEY, ADMIN_PASSWORD)
4. Railway auto-detects Procfile and deploys

## Architecture decisions

- **Triangulated scoring**: self 40% + manager 50% + peer 10%
- **70-20-10 paths**: stretch assignments first, courses last
- **4 skill tiers**: Core → Function → Role → Emerging
- **Living framework**: skill pools flagged for review every 90 days
