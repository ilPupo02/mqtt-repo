import paho.mqtt.client as mqtt
import random
import time
import json
import os
import sys
import logging

# Configure logging to see the output in Docker logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Read environment variables with validation
mqtt_broker = os.getenv("MQTT_BROKER")

if not mqtt_broker:
    logger.error("ERROR: MQTT_BROKER environment variable is not set.")
    sys.exit(1)

mqtt_port = int(os.getenv("MQTT_PORT", "1883"))
mqtt_username = os.getenv("MQTT_USERNAME", "test")
mqtt_password = os.getenv("MQTT_PASSWORD", "test")
mqtt_topic = os.getenv("MQTT_TOPIC", "sensor/visual_control")
mqtt_command_topic = os.getenv("MQTT_TOPIC_COMAND", "sensor/command")

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected to {mqtt_broker}:{mqtt_port} with result code {rc}")


# Global variable to store the break state
break_state = False

# Callback when the client receives a message
def on_message(client, userdata, msg):
    global break_state
    logger.info(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    
    # Check if the message is a command to break
    try:
        message = json.loads(msg.payload.decode())
        if "break" in message:
            break_state = message["break"]
            logger.info(f"Break state set to: {break_state}")
    except json.JSONDecodeError:
        logger.error("Failed to decode message, skipping")


# Initialize MQTT client
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(mqtt_broker, mqtt_port, 60)
except Exception as e:
    logger.error(f"ERROR: Connection failed to {mqtt_broker}:{mqtt_port} → {e}")
    sys.exit(1)

client.loop_start()

# Function to generate random data
def generate_visual_control_data():
    global break_state
    crack_rating_check = random.randint(1, 10)

    # If break state is True, set crack_rating to 10
    if break_state:
        crack_rating = 10
        break_state = False
    elif crack_rating_check > 8:
        crack_rating = random.randint(2, 10)
    else:
        crack_rating = 0
    
    return {
        "length": round(random.uniform(1.0, 2.0), 2),
        "width": round(random.uniform(0.5, 1.0), 2),
        "thickness": round(random.uniform(0.02, 0.05), 3),
        "crack_rating": crack_rating
    }

# Main loop
try:
    while True:
        data = generate_visual_control_data()
        message = json.dumps(data)
        client.publish(mqtt_topic, message)
        logger.info(f"Published: {message}")
        time.sleep(5)
except KeyboardInterrupt:
    logger.info("Exiting...")
finally:
    client.loop_stop()
    client.disconnect()
