import heapq
import time
import random

from domain.models import Status, AppointmentStage


STAGES = [
    AppointmentStage.INTAKE_VALIDATION,
    AppointmentStage.INSURANCE_ELIGIBILITY,
    AppointmentStage.CLINICAL_PRE_CHECK,
    AppointmentStage.PROVIDER_MATCHING,
    AppointmentStage.PATIENT_OUTREACH,
    AppointmentStage.FINALIZE_CONFIRM
]


class Orchestrator:
    def __init__(self, exception_queue):
        self.exception_queue = exception_queue

    def process(self, appointments):
        heap = [(a.priority, a) for a in appointments]
        heapq.heapify(heap)

        print("\n🚀 PIPELINE STARTED\n")

        while heap:
            _, appt = heapq.heappop(heap)

            print(f"\n➡️ Appointment {appt.id} - {appt.patient_name}")

            while appt.stage_index < len(STAGES):
                stage = STAGES[appt.stage_index]

                print(f"   🧠 Stage: {stage.value}")

                # simulate delay
                delay = random.uniform(0.5, 2.5)
                time.sleep(delay)

                result = self._simulate_stage(stage)

                print(f"   📌 Result: {result}")

                if result == Status.COMPLETE:
                    appt.stage_index += 1

                elif result == Status.ESCALATE:
                    appt.status = Status.ESCALATE
                    self.exception_queue.add(appt)
                    print(f"   🚨 ESCALATED at {stage.value}")
                    break

            if appt.stage_index == len(STAGES):
                appt.status = Status.COMPLETE
                print(f"✅ COMPLETED Appointment {appt.id}")

    def _simulate_stage(self, stage):
        if stage == AppointmentStage.INSURANCE_ELIGIBILITY:
            if random.random() < 0.3:
                return Status.ESCALATE

        if stage == AppointmentStage.PROVIDER_MATCHING:
            if random.random() < 0.2:
                return Status.ESCALATE

        return Status.COMPLETE