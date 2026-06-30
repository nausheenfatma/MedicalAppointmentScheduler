from enum import Enum


# -----------------------------
# STATUS (lifecycle state)
# -----------------------------
class Status(Enum):
    NOT_STARTED = "Not Started"
    PROCESSING = "Processing"
    COMPLETE = "Complete"
    ESCALATE = "Escalate"
    CLEARED = "Cleared"


# -----------------------------
# APPOINTMENT STAGES (workflow steps)
# -----------------------------
class AppointmentStage(Enum):
    INTAKE_VALIDATION = "Intake Validation"
    INSURANCE_ELIGIBILITY = "Insurance Eligibility"
    CLINICAL_PRE_CHECK = "Clinical Pre-check"
    PROVIDER_MATCHING = "Provider Matching"
    PATIENT_OUTREACH = "Patient Outreach"
    FINALIZE_CONFIRM = "Finalize & Confirm"


# -----------------------------
# DOMAIN MODEL
# -----------------------------
class Appointment:
    def __init__(
        self,
        id,
        patient_name,
        priority,
        stage_index=0,
        status=Status.NOT_STARTED
    ):
        self.id = id
        self.patient_name = patient_name
        self.priority = priority
        self.stage_index = stage_index
        self.status = status

    def __lt__(self, other):
        return self.priority < other.priority