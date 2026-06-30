from sqlalchemy import Column, Integer, String, Boolean, Float, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()




class AppointmentTable(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String)

    status = Column(String)
    stage_index = Column(Integer, default=0)

    # -----------------------------
    # NEW PRIORITY ENGINE FIELDS
    # -----------------------------
    client = Column(String, nullable=True)
    specialty = Column(String, nullable=True)

    vip = Column(Integer, default=0)
    risk_score = Column(Float, default=0.0)

    scheduled_ts = Column(BigInteger, nullable=True)

    priority = Column(Float, default=0.0)