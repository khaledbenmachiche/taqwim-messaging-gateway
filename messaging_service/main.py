import gammu
import json
import paho.mqtt.client as mqtt
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Configuration constants (use environment variables for sensitive data)
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt-broker")  # MQTT broker address
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "sms/outgoing")  # MQTT topic to subscribe to

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def send_sms(phone_number, message):
    """
    Sends an SMS using the Gammu library.

    Args:
        phone_number (str): The recipient's phone number.
        message (str): The message content to send.

    Raises:
        gammu.GSMError: If there is an issue with the Gammu state machine or SMS sending.
    """
    try:
        # Initialize the Gammu state machine
        sm = gammu.StateMachine()
        
        # Read the Gammu configuration file (usually ~/.gammurc)
        sm.ReadConfig()
        
        # Establish a connection to the modem
        sm.Init()
        
        # Prepare the SMS message payload
        sms = {
            "Text": message,  # The message content
            "SMSC": {"Location": 1},  # Use the default SMSC (message center)
            "Number": phone_number,  # Recipient's phone number
        }
        
        # Send the SMS
        sm.SendSMS(sms)
        logger.info(f"Message successfully sent to {phone_number}")
    
    except gammu.GSMError as e:
        # Handle Gammu-specific errors
        logger.error(f"Failed to send SMS to {phone_number}: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        logger.error(f"An unexpected error occurred while sending SMS: {e}")

def on_message(client, userdata, msg):
    """
    Callback function triggered when a message is received on the subscribed MQTT topic.

    Args:
        client: The MQTT client instance.
        userdata: User-defined data passed to the callback.
        msg: The received message object containing topic and payload.
    """
    try:
        # Decode the MQTT message payload (assumed to be JSON)
        payload = json.loads(msg.payload.decode())
        
        # Extract phone number and message from the payload
        phone_number = payload.get("phone_number", "").strip()
        message = payload.get("message", "").strip()
        
        # Validate the extracted data
        if not phone_number or not message:
            logger.error("Error: Invalid JSON payload. 'phone_number' and 'message' fields are required.")
            return
        
        # Send the SMS
        send_sms(phone_number, message)
    
    except json.JSONDecodeError:
        logger.error("Error: Failed to decode the received JSON payload.")
    except Exception as e:
        logger.error(f"An unexpected error occurred in the MQTT callback: {e}")

def main():
    """
    Main function to initialize the MQTT client and start the message loop.
    """
    try:
        # Initialize the MQTT client
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
        
        # Assign the on_message callback
        client.on_message = on_message
        
        # Connect to the MQTT broker
        client.connect(MQTT_BROKER, 1883, 60)
        
        # Subscribe to the specified topic
        client.subscribe(MQTT_TOPIC)
        logger.info(f"Subscribed to MQTT topic: {MQTT_TOPIC}")
        
        # Start the MQTT loop to process incoming messages
        client.loop_forever()
    
    except Exception as e:
        logger.error(f"An error occurred in the MQTT client setup: {e}")

if __name__ == "__main__":
    # Entry point of the script
    main()