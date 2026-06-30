from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.facade import WorkflowFacade
from domain.models import Status
from domain.orchestrator import STAGES

app = FastAPI()
facade = WorkflowFacade()

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# UI
# -----------------------------
app.mount("/ui", StaticFiles(directory="ui", html=True), name="ui")


# -----------------------------
# SAFE SERIALIZER
# -----------------------------
def safe_status(status):
    return status.value if hasattr(status, "value") else status


# -----------------------------
# PIPELINE
# -----------------------------
@app.post("/process-appointments")
def run_pipeline():
    result = facade.run_pipeline()
    return {"processed": len(result) if result else 0}


# -----------------------------
# APPOINTMENTS
# -----------------------------
@app.get("/appointments")
def get_appointments():
    appointments = facade.service.repo.fetch_all()

    return [
        {
            "id": a.id,
            "patient": a.patient_name,
            "priority": a.priority,
            "stage_index": a.stage_index,
            "status": a.status.value if hasattr(a.status, "value") else a.status
        }
        for a in appointments
    ]


# -----------------------------
# EXCEPTIONS
# -----------------------------
@app.get("/exceptions")
def get_exceptions():
    return [
        {
            "id": a.id,
            "patient": a.patient_name,
            "stage": (
                STAGES[a.stage_index].value
                if a.stage_index < len(STAGES)
                else "Unknown"
            ),
            "status": safe_status(a.status),
        }
        for a in facade.service.repo.fetch_all()
        if a.status == Status.ESCALATE
    ]


# -----------------------------
# RESOLVE (Human Concierge)
# -----------------------------
@app.post("/resolve-exception/{id}")
def resolve(id: int):
    return facade.resolve_exception(id)


@app.post("/set-priority-mode")
def set_priority_mode(mode: str):
    """
    mode:
    - heuristic
    - llm
    """
    facade.service.priority_engine.use_llm = (mode == "heuristic")
    return {"mode": mode}