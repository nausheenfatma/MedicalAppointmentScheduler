from services.workflow_service import WorkflowService


class WorkflowFacade:
    def __init__(self):
        self.service = WorkflowService()

    def run_pipeline(self):
        return self.service.process_all()

    def get_exception_queue(self):
        return self.service.get_exceptions()

    def resolve_exception(self, appointment_id):
        self.service.resolve(appointment_id)