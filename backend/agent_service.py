import os
import base64
import requests

from dotenv import load_dotenv
from agora_agent import Agora,Agent,Area

from token_service import generate_rtc_token

load_dotenv()


AGORA_APP_ID = os.getenv("AGORA_APP_ID")

AGORA_APP_CERTIFICATE = os.getenv("AGORA_APP_CERTIFICATE")

AGORA_PIPELINE_ID = os.getenv("AGORA_PIPELINE_ID")

AGORA_CUSTOMER_ID = os.getenv(
    "AGORA_CUSTOMER_ID"
)

AGORA_CUSTOMER_SECRET = os.getenv(
    "AGORA_CUSTOMER_SECRET"
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

AGORA_AGENT_UID = os.getenv(
        "AGORA_AGENT_UID",
        "999001"
    )



class AgoraAgentService:

    def __init__(self):
        self.client = Agora(
            area=Area.US,
            app_id=AGORA_APP_ID,
            app_certificate=AGORA_APP_CERTIFICATE
        )

        self.agent = Agent(
            client=self.client,
            pipeline_id=AGORA_PIPELINE_ID,
        )

        self.sessions = {}

    def start_agent(
            self,
            incident_id:str,
            channel_name:str
    ):
        session = self.agent.create_session(
            channel=channel_name,
            agent_uid=str(AGORA_AGENT_UID),

            remote_uids=["*"],

            name=f"incident-commander-{incident_id}",
            idle_timeout=600,
        )

        agent_id = session.start()
        self.sessions[incident_id]=session 

        print("===============================")
        print("AI INCIDENT COMMANDER STARTED")
        print("Incident:",incident_id)
        print("Channel:",channel_name)
        print("Agent UID:",AGORA_AGENT_UID)
        print("Agent ID:",agent_id)
        print("================================")

        return{
            "status":"started",
            "agent_id":agent_id,
            "channel":channel_name,
            "agent_uid":AGORA_AGENT_UID
        }
agora_agent_service = AgoraAgentService()

#     def _authorization_header(self):

#         credentials = (
#             f"{AGORA_CUSTOMER_ID}:"
#             f"{AGORA_CUSTOMER_SECRET}"
#         )

#         encoded = base64.b64encode(
#             credentials.encode()
#         ).decode()

#         return f"Basic {encoded}"

#     def start_agent(
#         self,
#         incident_id: str,
#         channel_name: str
#     ):

#         # Generate RTC token
#         # specifically for the AI agent UID.

#         agent_token_data = generate_rtc_token(
#             channel_name=channel_name,
#             uid=AGENT_UID
#         )

#         agent_token = (
#             agent_token_data["token"]
#         )

#         url = (
#             "https://api.agora.io/"
#             "api/conversational-ai-agent/"
#             f"v2/projects/{AGORA_APP_ID}/join"
#         )


#         payload = {

#             "name":
#                 f"incident-commander-{incident_id}",

#            "properties": {

#     "channel": channel_name,

#     "token": agent_token,

#     "agent_rtc_uid": str(
#         AGENT_UID
#     ),

#     "remote_rtc_uids": [
#         "*"
#     ],

#     "enable_rtm": True,

#     "mllm": {
#         "enable": True,
#         "api_key": GEMINI_API_KEY,
#         "vendor": "gemini",

#         "params": {
#             "model":
#                 "gemini-3.1-flash-live-preview",

#             "instructions": (
#                 "You are an AI Incident Commander "
#                 "inside a live technical incident room"
#                 "Listen carefully to all participants. Do not invent facts."
#                 "Do not interrupt unnecessarily. When directly addressed, respond"
#                 "briefly and professionally."
#             ),

#             "voice":
#                 "Charon",

#             "transcribe_agent": True,
#             "transcribe_user": True,

#             "http_options": {
#                 "api_version": "v1beta"
#             }
#         },

#         "input_modalities": [
#             "audio"
#         ],

#         "output_modalities": [
#             "audio"
#         ],

        
#     }
# }
#         }


#         headers = {

#             "Authorization":
#                 self._authorization_header(),

#             "Content-Type":
#                 "application/json"
#         }


#         print(
#             "Starting Agora AI agent..."
#         )

#         print(
#             "Channel:",
#             channel_name
#         )

#         print(
#             "Agent UID:",
#             AGENT_UID
#         )


#         response = requests.post(
#             url,
#             json=payload,
#             headers=headers,
#             timeout=30
#         )


#         print(
#             "Agora status:",
#             response.status_code
#         )

#         print(
#             "Agora response:",
#             response.text
#         )


#         if not response.ok:

#             raise RuntimeError(
#                 f"Agora agent error "
#                 f"{response.status_code}: "
#                 f"{response.text}"
#             )


#         data = response.json()


#         self.active_agents[
#             incident_id
#         ] = data


#         return data
