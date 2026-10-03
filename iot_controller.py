import paho.mqtt.client as mqtt
import time

# These must match the exact broker and topic defined in your FastAPI main.py
MQTT_BROKER = "localhost" 
MQTT_TOPIC = "gate/control"

def on_connect(client, userdata, flags, rc):
    """Callback triggered when the client connects to the broker."""
    if rc == 0:
        print(f"[SUCCESS] Connected to MQTT broker at {MQTT_BROKER}")
        # Subscribe to the topic immediately upon connection
        client.subscribe(MQTT_TOPIC)
        print(f"[INFO] Listening for access signals on topic: '{MQTT_TOPIC}'...\n")
    else:
        print(f"[ERROR] Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    """Callback triggered whenever a message is published to a subscribed topic."""
    payload = msg.payload.decode("utf-8")
    print(f"[{time.strftime('%H:%M:%S')}] Signal received: {payload}")
    
    if payload == "OPEN_GATE":
        # Visual indicator for testing
        print("="*40)
        print(">>> TRIGGERING 5V RELAY: GATE OPENING <<<")
        print("="*40)
        
        # In a real hardware deployment on a Raspberry Pi, you would replace the print 
        # statements with GPIO commands:
        # GPIO.output(RELAY_PIN, GPIO.HIGH)
        # time.sleep(5) # Keep gate open for 5 seconds
        # GPIO.output(RELAY_PIN, GPIO.LOW)
    else:
        print("[WARNING] Unrecognized command received.")

# Initialize the MQTT client
client = mqtt.Client()

# Attach the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker and start listening indefinitely
try:
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()
except ConnectionRefusedError:
    print("[ERROR] Connection refused. Is your MQTT broker (e.g., Mosquitto) running?")
except KeyboardInterrupt:
    print("\n[INFO] Shutting down IoT controller simulator.")
    client.disconnect()