from infrastructure.db.connection import SessionLocal
from infrastructure.db.models import AppointmentTable
from domain.models import Appointment, Status


class AppointmentRepository:

    def fetch_all(self):
        session = SessionLocal()
        try:
            rows = session.query(AppointmentTable).all()

            return [
                Appointment(
                    id=r.id,
                    patient_name=r.patient_name,
                    priority=r.priority,
                    stage_index=r.stage_index,

                    status=Status(r.status) if r.status else Status.NOT_STARTED
                )
                for r in rows
            ]
        finally:
            session.close()

    def update(self, appointment):
        session = SessionLocal()
        try:
            db_obj = session.query(AppointmentTable).filter_by(id=appointment.id).first()

            if db_obj:
                db_obj.priority = appointment.priority

                # Enum → string for DB
                db_obj.status = appointment.status.value

                db_obj.stage_index = appointment.stage_index

            session.commit()
        finally:
            session.close()