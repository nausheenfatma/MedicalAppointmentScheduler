class ExceptionQueue:
    def __init__(self):
        self.queue = []

    def add(self, appointment):
        self.queue.append(appointment)

    def get_all(self):
        return self.queue


class HumanConcierge:
    def resolve(self, appointment):
        appointment.status = "Cleared"
        return appointment