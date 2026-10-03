from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from database import Base

class GatePass(Base):
    __tablename__ = "gate_passes"
    plate_number = Column(String(20), primary_key=True, index=True)
    vehicle_type = Column(String(50))
    owner_id = Column(String(50))
    is_active = Column(Boolean, default=True)

class AccessLog(Base):
    __tablename__ = "access_logs"
    log_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    plate_number = Column(String(20))
    detected_type = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    access_granted = Column(Boolean)
    reason = Column(String(100))