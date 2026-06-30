import time


class PriorityEngine:
    def __init__(self, use_llm=False, llm_client=None):
        self.use_llm = use_llm
        self.llm_client = llm_client

    def compute_priority(self, appt: dict) -> float:
        if self.use_llm:
            return self._llm_score(appt)
        return self._heuristic_score(appt)

    def _heuristic_score(self, appt: dict) -> float:
        now = int(time.time())

        scheduled_ts = appt.get("scheduled_ts", now + 3600)
        time_to_appt = max(1, scheduled_ts - now)
        hours_to_appt = time_to_appt / 3600.0

        client_weight = {
            "NorthCare": 1.1,
            "SunriseHealth": 1.0,
            "BlueCrossClinic": 0.95
        }.get(appt.get("client"), 1.0)

        specialty_weight = {
            "Oncology": 1.25,
            "Cardiology": 1.15,
            "Pediatrics": 1.05
        }.get(appt.get("specialty"), 1.0)

        score = 0.0
        score += appt.get("vip", 0) * 30
        score += appt.get("risk_score", 0) * 0.6
        score += max(0, (72 - hours_to_appt))
        score *= client_weight * specialty_weight

        return score

    def _llm_score(self, appt: dict) -> float:
        prompt = f"""
        You are a medical triage system.
        Return a priority score (0-100).

        Appointment:
        {appt}

        Only return number.
        """

        try:
            response = self.llm_client.invoke(prompt)
            return float(response.strip())
        except:
            return self._heuristic_score(appt)