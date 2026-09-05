from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from token_service import generate_rtc_token
from transcript_service import transcript_service
from agent_service import agora_agent_service


app = FastAPI(
    title="AI Incident Commander"
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


class TokenRequest(BaseModel):
    channel: str
    uid: int


class ParticipantRequest(BaseModel):
    uid: str
    name: str
    role: str
    team: str | None = None


class StartAgentRequest(BaseModel):
    channel: str


class TranscriptRequest(BaseModel):
    uid: str
    text: str
    is_final: bool = True
    start_time: str | None = None
    end_time: str | None = None


@app.get("/")
def health():

    return {
        "status": "ok",
        "service": "incident-commander"
    }


# -------------------------
# Agora RTC Token
# -------------------------

@app.post("/api/agora/token")
def create_token(
    request: TokenRequest
):

    try:

        return generate_rtc_token(
            channel_name=request.channel,
            uid=request.uid
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# -------------------------
# Participant roster
# -------------------------

@app.post(
    "/api/incidents/"
    "{incident_id}/participants"
)
def add_participant(
    incident_id: str,
    request: ParticipantRequest
):

    try:
        print("INCIDENT ID:",incident_id)
        print("REQUEST:",request)
        print("SERVICE:",transcript_service)
        participant = (
            transcript_service
            .add_participant(
                incident_id=incident_id,

                uid=request.uid,

                name=request.name,

                role=request.role,

                team=request.team
            )
        )

        return {
            "success": True,
            "participant": participant
        }
    except Exception as e:
        print("ERROR IN add_participant:",repr(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



@app.get(
    "/api/incidents/"
    "{incident_id}/participants"
)
def get_participants(
    incident_id: str
):

    return {
        "participants":
            transcript_service
            .get_roster(
                incident_id
            )
    }


# -------------------------
# Start AI Agent
# -------------------------

@app.post(
    "/api/incidents/"
    "{incident_id}/start-agent"
)
def start_agent(
    incident_id: str,
    request: StartAgentRequest
):

    try:

        result = (
            agora_agent_service
            .start_agent(
                incident_id=
                    incident_id,

                channel_name=
                    request.channel
            )
        )

        return {
            "success": True,
            "agent": result
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# -------------------------
# Transcript ingestion
# -------------------------

@app.post(
    "/api/incidents/"
    "{incident_id}/transcripts"
)
async def ingest_transcript(
    incident_id: str,
    request: TranscriptRequest
):

    event = (
        await transcript_service
        .on_transcript_message(
            incident_id,

            request.model_dump()
        )
    )

    return {
        "processed": (
            event is not None
        ),

        "event": event
    }


@app.get(
    "/api/incidents/"
    "{incident_id}/transcripts"
)
def get_transcripts(
    incident_id: str
):

    return {
        "transcripts":
            transcript_service
            .get_transcripts(
                incident_id
            )
    }