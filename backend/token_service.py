import os
import time

from dotenv import load_dotenv
from agora_token_builder import RtcTokenBuilder

load_dotenv()

AGORA_APP_ID = os.getenv("AGORA_APP_ID")
AGORA_APP_CERTIFICATE = os.getenv("AGORA_APP_CERTIFICATE")

def generate_rtc_token(
        channel_name: str,
        uid: int,
        expiration_seconds:int = 3600
):
    if not AGORA_APP_ID:
        raise RuntimeError("AGORA_APP_ID is missing")

    if not AGORA_APP_CERTIFICATE:
        raise RuntimeError("AGORA_APP_CERTIFICATE is missing")

    current_timestamp = int(time.time())

    privilege_expired_timestamp = (
        current_timestamp + expiration_seconds
    )

    role = 1 #RTC subscriber/publisher role

    token = RtcTokenBuilder.buildTokenWithUid(
        AGORA_APP_ID,
        AGORA_APP_CERTIFICATE,
        channel_name,
        uid,
        role,
        privilege_expired_timestamp
    )

    return {
        "appId":AGORA_APP_ID,
        "token":token,
        "channel":channel_name,
        "uid":uid
    }