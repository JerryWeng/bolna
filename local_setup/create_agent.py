import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the Bolna ngrok URL from environment
bolna_ngrok_url = os.getenv("BOLNA_NGROK_URL")
if not bolna_ngrok_url:
    print("ERROR: BOLNA_NGROK_URL not found in environment variables")
    exit(1)

# Check if Deepgram API key exists in environment
deepgram_key = os.getenv("DEEPGRAM_AUTH_TOKEN")
if not deepgram_key:
    print("WARNING: DEEPGRAM_AUTH_TOKEN not found in environment variables")
    print("This may cause issues with transcription. Make sure it's in your .env file.")

# Full URL for the agent creation endpoint
bolna_url = f"https://{bolna_ngrok_url}/agent"

# Payload for creating a Deepgram-based agent
deepgram_agent_config = {
  "agent_config": {
    "agent_name": "Deepgram Phone Agent",
    "agent_type": "other",
    "agent_welcome_message": "Hello, this is an AI assistant calling. How are you doing today?",
    "tasks": [
      {
        "task_type": "conversation",
        "toolchain": {
          "execution": "sequential",
          "pipelines": [
            [
              "transcriber",
              "llm",
              "synthesizer"
            ]
          ]
        },
        "tools_config": {
          "input": {
            "format": "wav",
            "provider": "twilio"
          },
          "llm_agent": {
            "agent_type": "simple_llm_agent",
            "agent_flow_type": "streaming",
            "routes": None,
            "llm_config": {
              "agent_flow_type": "streaming",
              "provider": "openai",
              "request_json": True,
              "model": "gpt-4.1"
            }
          },
          "output": {
            "format": "wav",
            "provider": "twilio"
          },
          "synthesizer": {
            "audio_format": "wav",
            "provider": "openai",
            "stream": True,
            "provider_config": {
              "voice": "alloy",
              "model": "tts-1"
            },
            "buffer_size": 100.0
          },
          "transcriber": {
            "provider": "deepgram",
            "language": "en-US",
            "stream": True,
            "encoding": "linear16",
            "sampling_rate": 16000
          }
        },
        "task_config": {
          "hangup_after_silence": 30.0,
          "check_if_user_online": True,
          "trigger_user_online_message_after": 10,
          "optimize_latency": False
        }
      }
    ]
  },
  "agent_prompts": {
    "task_1": {
      "system_prompt": "You are a friendly and helpful AI assistant making a phone call. Engage the person in conversation and respond thoughtfully to their questions. Be natural and conversational. If you don't hear a response for a while, ask if they're still there."
    }
  }
}

# Create the agent
print(f"Creating Deepgram agent via {bolna_url}...")
try:
    response = requests.post(bolna_url, json=deepgram_agent_config)
    
    # Print response details
    print(f"Status code: {response.status_code}")
    print(f"Response text: {response.text}")
    
    # If successful, parse the JSON response
    if response.status_code == 200:
        try:
            agent_response = response.json()
            
            # Extract and save the agent ID
            if 'agent_id' in agent_response:
                new_agent_id = agent_response['agent_id']
                print(f"Created agent with ID: {new_agent_id}")
                
                # Update the ASSISTANT_ID in .env file
                env_lines = []
                with open('.env', 'r') as file:
                    env_lines = file.readlines()
                
                with open('.env', 'w') as file:
                    updated = False
                    for line in env_lines:
                        if line.startswith('ASSISTANT_ID='):
                            file.write(f'ASSISTANT_ID={new_agent_id}\n')
                            updated = True
                        else:
                            file.write(line)
                    
                    # Add ASSISTANT_ID if it didn't exist
                    if not updated:
                        file.write(f'\nASSISTANT_ID={new_agent_id}\n')
                
                print(f"Updated ASSISTANT_ID in .env file")
                print("\nYou can now make a call:")
                print("python make_call.py")
            else:
                print("Agent created but no agent_id found in response.")
        except json.JSONDecodeError:
            print("Could not parse response as JSON")
    else:
        print(f"Failed to create agent. Status code: {response.status_code}")
except Exception as e:
    print(f"Error creating agent: {str(e)}")