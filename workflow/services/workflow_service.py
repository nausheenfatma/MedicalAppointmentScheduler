from domain.orchestrator import Orchestrator
from domain.exceptions import ExceptionQueue
from infrastructure.db.appointment_repo import AppointmentRepository
from domain.priority_engine import PriorityEngine
import time


class WorkflowService:
    def __init__(self):
        self.repo = AppointmentRepository()
        self.exception_queue = ExceptionQueue()

        # priority engine (default heuristic mode)
        self.priority_engine = PriorityEngine(use_llm=False)

        self.orchestrator = Orchestrator(self.exception_queue)

    def process_all(self):
        appts = self.repo.fetch_all()

        enriched = []

        # -----------------------------
        # COMPUTE DYNAMIC PRIORITIES
        # -----------------------------
        for a in appts:
            appt_dict = {
                "id": a.id,
                "client": getattr(a, "client", "Unknown"),
                "specialty": getattr(a, "specialty", "General"),
                "vip": getattr(a, "vip", 0),
                "risk_score": getattr(a, "risk_score", 0),
                "scheduled_ts": getattr(a, "scheduled_ts", int(time.time()) + 3600),
            }

            a.priority = self.priority_engine.compute_priority(appt_dict)
            enriched.append(a)

        # run orchestrator
        self.orchestrator.process(enriched)

        # persist updates
        for a in enriched:
            self.repo.update(a)

        return enriched

    def get_exceptions(self):
        return [a for a in self.repo.fetch_all() if a.status.value == "Escalate"]

    def resolve(self, appointment_id):
        for a in self.repo.fetch_all():
            if a.id == appointment_id:
                a.status = a.status.__class__.CLEARED
                self.repo.update(a)
                return a