from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
import paho.mqtt.client as mqtt
from datetime import datetime

from database import SessionLocal, engine, Base
import models
from ai_pipeline import process_image

# Generate database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="University Gate Access API")

# Setup MQTT Client for hardware communication
MQTT_BROKER = "localhost" # Change to your broker IP (e.g., Raspberry Pi IP)
MQTT_TOPIC = "gate/control"
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, 1883, 60)

# Dependency to inject DB sessions safely
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/v1/gate/verify")
async def verify_vehicle(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Ingest image from edge camera
    image_bytes = await file.read()

    # 2. Run AI Inference
    detected_type, plate_number = process_image(image_bytes)

    # 3. Validation Logic
    gate_pass = db.query(models.GatePass).filter(models.GatePass.plate_number == plate_number).first()
    
    access_granted = False
    reason = "Plate not registered"

    if gate_pass:
        if not gate_pass.is_active:
            reason = "Pass is currently inactive"
        elif gate_pass.vehicle_type.lower() != detected_type.lower():
            reason = f"Mismatch: Registered as {gate_pass.vehicle_type}, detected as {detected_type}"
        else:
            access_granted = True
            reason = "Access granted"

    # 4. Hardware Trigger
    if access_granted:
        mqtt_client.publish(MQTT_TOPIC, "OPEN_GATE")

    # 5. Audit Logging
    new_log = models.AccessLog(
        plate_number=plate_number,
        detected_type=detected_type,
        timestamp=datetime.utcnow(),
        access_granted=access_granted,
        reason=reason
    )
    db.add(new_log)
    db.commit()

    # 6. API Response
    return {
        "access": access_granted,
        "plate_number": plate_number,
        "detected_type": detected_type,
        "reason": reason
    }