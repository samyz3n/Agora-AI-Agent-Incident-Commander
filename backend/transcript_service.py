from datetime import datetime, timezone


class TranscriptService:

    def __init__(self):
        self.rosters = {}
        self.transcripts = {}

    def add_participant(
        self,
        incident_id: str,
        uid: str,
        name: str,
        role: str,
        team: str | None = None
    ):
        if incident_id not in self.rosters:
            self.rosters[incident_id] = {}

        self.rosters[incident_id][uid] = {
            "uid": uid,
            "name": name,
            "role": role,
            "team": team
        }

        return self.rosters[incident_id][uid]

    def remove_participant(
        self,
        incident_id: str,
        uid: str
    ):
        if incident_id not in self.rosters:
            return

        self.rosters[incident_id].pop(uid, None)

    def get_roster(self, incident_id: str):
        return list(
            self.rosters.get(
                incident_id,
                {}
            ).values()
        )

    async def on_transcript_message(
        self,
        incident_id: str,
        msg: dict
    ):
        """
        Expected Agora transcript shape:

        {
            "uid": "1042",
            "text": "...",
            "is_final": true,
            "start_time": "...",
            "end_time": "..."
        }
        """

        # IMPORTANT:
        # Ignore partial ASR results.
        if not msg.get("is_final"):
            return None

        uid = str(msg.get("uid"))

        participant = (
            self.rosters
            .get(incident_id, {})
            .get(uid)
        )

        if participant:
            speaker = participant
        else:
            speaker = {
                "uid": uid,
                "name": "Unknown participant",
                "role": "unknown",
                "team": None
            }

        event = {
            "incident_id": incident_id,

            "speaker": speaker,

            "text": msg.get("text", ""),

            "timestamp": (
                msg.get("end_time")
                or datetime.now(
                    timezone.utc
                ).isoformat()
            )
        }

        if incident_id not in self.transcripts:
            self.transcripts[incident_id] = []

        self.transcripts[
            incident_id
        ].append(event)

        print("\n==============================")
        print("FINAL TRANSCRIPT")
        print("==============================")
        print(
            f"{speaker['name']} "
            f"({speaker['role']})"
        )
        print(event["text"])
        print("==============================\n")

        # Later:
        #
        # await publish_to_queue(
        #     "transcript.raw",
        #     event
        # )
        #
        # Do NOT call the LLM here yet.

        return event

    def get_transcripts(
        self,
        incident_id: str
    ):
        return self.transcripts.get(
            incident_id,
            []
        )


transcript_service = TranscriptService()