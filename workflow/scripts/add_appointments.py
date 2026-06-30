import random
from infrastructure.db.connection import SessionLocal
from infrastructure.db.models import AppointmentTable


# -----------------------------
# NAME GENERATION
# -----------------------------
first_names = [
    "Alex", "Jordan", "Taylor", "Morgan", "Casey",
    "Riley", "Avery", "Jamie", "Drew", "Parker",
    "Cameron", "Reese", "Quinn", "Rowan", "Skyler"
]

last_names = [
    "Smith", "Johnson", "Brown", "Taylor", "Anderson",
    "Thomas", "Jackson", "White", "Harris", "Martin",
    "Thompson", "Garcia", "Martinez", "Robinson", "Clark"
]


def generate_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"


# -----------------------------
# SAMPLE CONTEXT DATA (NEW)
# -----------------------------
CLIENTS = ["NorthCare", "SunriseHealth", "BlueCrossClinic"]
SPECIALTIES = ["Oncology", "Cardiology", "Pediatrics", "General"]


def run(n=10):
    session = SessionLocal()

    for _ in range(n):
        session.add(AppointmentTable(
            patient_name=generate_name(),


            priority=0, #default priority is same 0, will be computed dynamically by PriorityEngine

            status="Not Started",
            stage_index=0,

            # NEW: fields used by PriorityEngine
            client=random.choice(CLIENTS),
            specialty=random.choice(SPECIALTIES),
            vip=random.randint(0, 1),
            risk_score=round(random.uniform(0, 10), 2),
            scheduled_ts=int(random.time() if hasattr(random, "time") else __import__("time").time()) + random.randint(3600, 200000)
        ))

    session.commit()
    session.close()

    print("Inserted appointments (raw data only)")


if __name__ == "__main__":
    run(10)