"""
Bootstrap router — seed check and status
"""
from fastapi import APIRouter
from backend.services.storage import read_json
from backend.models.schemas import BootstrapResponse

router = APIRouter()


@router.post("/bootstrap", response_model=BootstrapResponse)
def bootstrap():
    """
    Read-only seed check. Returns counts from the three core data files.
    Idempotent — safe to call multiple times.
    """
    try:
        org = read_json("org_structure.json")
        framework = read_json("skill_framework.json")
        employees = read_json("employees.json")
        assessments = read_json("assessments.json")
    except FileNotFoundError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Data file missing: {e}")

    functions = org.get("functions", [])
    roles_count = sum(
        len(fn.get("roles", {}))
        for fn in framework.get("functions", {}).values()
    )

    return BootstrapResponse(
        status="ok",
        functions_loaded=len(functions),
        roles_loaded=roles_count,
        employees_loaded=len(employees.get("employees", [])),
        assessments_loaded=len(assessments.get("assessments", [])),
    )
