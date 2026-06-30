import random
from domain.models import Status


class Agent:
    def __init__(self, name):
        self.name = name

    def process(self, appointment):
        appointment.status = Status.PROCESSING

        if random.random() < 0.2:
            appointment.status = Status.ESCALATE
            return Status.ESCALATE

        appointment.status = Status.COMPLETE
        return Status.COMPLETE