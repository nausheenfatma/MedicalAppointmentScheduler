from enum import Enum
import random
import heapq


# -----------------------------
# STANDARD STATES
# -----------------------------
class Status(Enum):
    NOT_STARTED = "Not Started"
    PROCESSING = "Processing"
    COMPLETE = "Complete"
    ESCALATE = "Escalate"
    CLEARED = "Cleared"


# -----------------------------
# APPOINTMENT MODEL
# -----------------------------
class Appointment:
    def __init__(self, id, patient_name, priority):
        self.id = id
        self.patient_name = patient_name
        self.priority = priority  # Lower = higher priority
        self.stage_index = 0
        self.status = Status.NOT_STARTED

    def __lt__(self, other):
        return self.priority < other.priority

    def __repr__(self):
        return f"[Appt {self.id} | {self.patient_name} | Stage {self.stage_index} | {self.status.value}]"


# -----------------------------
# AGENT (STAGE PROCESSOR)
# -----------------------------
class Agent:
    def __init__(self, name):
        self.name = name

    def process(self, appointment):
        print(f"{self.name} processing {appointment}")

        appointment.status = Status.PROCESSING

        # Simulate random outcome
        outcome = random.choice([
            Status.COMPLETE,
            Status.COMPLETE,
            Status.ESCALATE  # small chance of escalation
        ])

        appointment.status = outcome

        return outcome


# -----------------------------
# EXCEPTION QUEUE
# -----------------------------
class ExceptionQueue:
    def __init__(self):
        self.queue = []

    def add(self, appointment):
        print(f"🚨 Escalated: {appointment}")
        self.queue.append(appointment)

    def get_all(self):
        return self.queue


# -----------------------------
# HUMAN CONCIERGE
# -----------------------------
class HumanConcierge:
    def resolve(self, appointment):
        print(f"👩‍⚕️ Resolving {appointment}")
        appointment.status = Status.CLEARED
        return appointment


# -----------------------------
# ORCHESTRATOR
# -----------------------------
class Orchestrator:
    def __init__(self, agents):
        self.agents = agents
        self.exception_queue = ExceptionQueue()
        self.concierge = HumanConcierge()

    def process_appointments(self, appointments):
        heapq.heapify(appointments)

        while appointments:
            appointment = heapq.heappop(appointments)
            print(f"\n➡️ Processing {appointment}")

            while appointment.stage_index < len(self.agents):
                agent = self.agents[appointment.stage_index]

                result = agent.process(appointment)

                if result == Status.COMPLETE:
                    appointment.stage_index += 1

                elif result == Status.ESCALATE:
                    self.exception_queue.add(appointment)
                    break

            if appointment.stage_index == len(self.agents):
                print(f"✅ Completed: {appointment}")

    def resolve_exceptions(self):
        for appointment in self.exception_queue.get_all():
            self.concierge.resolve(appointment)

            # Resume workflow after resolution
            print(f"🔁 Resuming {appointment}")
            while appointment.stage_index < len(self.agents):
                agent = self.agents[appointment.stage_index]
                result = agent.process(appointment)

                if result == Status.COMPLETE:
                    appointment.stage_index += 1
                else:
                    print(f"⚠️ Escalated again: {appointment}")
                    break

            if appointment.stage_index == len(self.agents):
                print(f"✅ Completed after resolution: {appointment}")


# -----------------------------
# DEMO
# -----------------------------
if __name__ == "__main__":
    # Create agents (6 stages)
    agents = [Agent(f"Agent {i}") for i in range(1, 7)]

    orchestrator = Orchestrator(agents)

    # Mock appointments (priority-driven)
    appointments = [
        Appointment(1, "Alice", priority=2),
        Appointment(2, "Bob", priority=1),
        Appointment(3, "Charlie", priority=3),
    ]

    print("=== START PROCESSING ===")
    orchestrator.process_appointments(appointments)

    print("\n=== EXCEPTION QUEUE ===")
    for appt in orchestrator.exception_queue.get_all():
        print(appt)

    print("\n=== HUMAN RESOLUTION ===")
    orchestrator.resolve_exceptions()