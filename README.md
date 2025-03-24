# SMS MQTT Gateway

This project is a Python-based SMS gateway that listens to an MQTT topic for incoming messages and sends them via a GSM modem using the Gammu library.

## Features
- Listens to an MQTT broker for incoming SMS messages.
- Sends SMS messages using Gammu.
- Configurable via environment variables.
- Logs message sending status and errors.

## Prerequisites
- A GSM modem compatible with Gammu.
- An MQTT broker (e.g., Mosquitto).
- Python 3 installed with required dependencies.

## Installation
1. Clone the repository:
   ```bash
   git clone git@github.com:khaledbenmachiche/taqwim-messaging-gateway.git
   cd taqwim-messaging-gateway
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure Gammu by setting up a `~/.gammurc` file with the correct modem settings.
4. Create a `.env` file to configure MQTT settings:
   ```ini
   MQTT_BROKER=mqtt-broker
   MQTT_TOPIC=sms/outgoing
   ```

## Usage
Run the script:
```bash
python sms_gateway.py
```

## Environment Variables
- `MQTT_BROKER`: Address of the MQTT broker.
- `MQTT_TOPIC`: Topic to listen for incoming SMS messages.

## MQTT Message Format
The script expects messages in JSON format with the following structure:
```json
{
    "phone_number": "+1234567890",
    "message": "Hello, this is a test SMS!"
}
```

## Logging
Logs are printed to the console and include timestamps, message statuses, and errors.

## Troubleshooting
- Ensure the modem is properly configured with Gammu (`gammu --identify`).
- Check MQTT broker connectivity.
- Verify the `.env` file has correct values.

## License
This project is licensed under the MIT License.


