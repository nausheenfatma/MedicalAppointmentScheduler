# ui/console_ui.py

from app.facade import WorkflowFacade

facade = WorkflowFacade()

facade.run_pipeline()

print("\nException Queue:")
exceptions = facade.get_exception_queue()

for appt in exceptions:
    print(appt.id, appt.patient_name)

# Simulate human resolving
if exceptions:
    facade.resolve_exception(exceptions[0].id)