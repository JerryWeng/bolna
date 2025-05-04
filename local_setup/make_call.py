import requests
import os
import json
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("call_debug.log"), 
                              logging.StreamHandler()])
logger = logging.getLogger("bolna_debug")

load_dotenv()

# Load destination phone number from .env
destination_number = os.getenv('DESTINATION_PHONE_NUMBER')
agent_id = os.getenv('ASSISTANT_ID')

# Get the ngrok URL for your twilio-app (not the bolna-app)
twilio_app_url = os.getenv('TWILIO_NGROK_URL')

# Log environment variables (excluding sensitive ones)
logger.info(f"BOLNA_NGROK_URL: {os.getenv('BOLNA_NGROK_URL')}")
logger.info(f"TWILIO_NGROK_URL: {twilio_app_url}")
logger.info(f"ASSISTANT_ID: {agent_id}")
logger.info(f"Using destination number: {destination_number[:6]}****")  # Partially masked for privacy

# Prepare the payload
payload = {
    "agent_id": agent_id,
    "recipient_phone_number": destination_number,
    "debug_mode": True  # Enable debug if supported
}

logger.info(f"Preparing to make call with payload: {json.dumps(payload)}")

# Make the request
try:
    logger.info(f"Sending request to {twilio_app_url}/call")
    response = requests.post(f"{twilio_app_url}/call", json=payload)
    
    logger.info(f"Status code: {response.status_code}")
    logger.info(f"Response headers: {response.headers}")
    logger.info(f"Response: {response.text}")
    
    # Try to parse the response as JSON
    if response.text.strip():
        try:
            json_response = response.json()
            logger.info(f"JSON response: {json.dumps(json_response, indent=2)}")
        except json.JSONDecodeError:
            logger.warning("Could not parse response as JSON")
    
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
    
except Exception as e:
    logger.error(f"Exception occurred: {str(e)}", exc_info=True)
    print(f"Error: {str(e)}")