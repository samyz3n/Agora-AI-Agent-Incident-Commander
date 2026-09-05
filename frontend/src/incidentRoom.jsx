import {
    useEffect,
    useState
} from "react";

import {
    getAgoraToken,
    registerParticipant,
    startAgent
} from "./api";

import {
    joinAgoraRoom,
    setupRemoteAudio,
    setMuted,
    leaveAgoraRoom
} from "./agora";


export default function IncidentRoom() {

    const [
        name,
        setName
    ] = useState("");

    const [
        role,
        setRole
    ] = useState(
        "on-call-sre"
    );

    const [
        team,
        setTeam
    ] = useState(
        "payments"
    );

    const [
        incidentId,
        setIncidentId
    ] = useState(
        "incident-4821"
    );

    const [
        joined,
        setJoined
    ] = useState(false);

    const [
        muted,
        setMutedState
    ] = useState(false);

    const [
        uid,
        setUid
    ] = useState(null);

    const [
        agentStarted,
        setAgentStarted
    ] = useState(false);

    const [
        status,
        setStatus
    ] = useState(
        "Not connected"
    );


    useEffect(() => {

        setupRemoteAudio();

    }, []);


    async function handleJoin() {

        try {

            if (!name.trim()) {

                alert(
                    "Enter your name"
                );

                return;
            }

            setStatus(
                "Connecting..."
            );

            // Hackathon MVP.
            // Backend-generated UID
            // would be better later.

            const generatedUid =
                Math.floor(
                    1000 +
                    Math.random() *
                    8000
                );

            setUid(
                generatedUid
            );


            // Register participant
            // BEFORE joining.

            await registerParticipant(
                incidentId,
                {
                    uid:
                        String(
                            generatedUid
                        ),

                    name,
                    role,
                    team
                }
            );


            // Get token.

            const tokenData =
                await getAgoraToken(
                    incidentId,
                    generatedUid
                );

            console.log("TOKEN DATA:", tokenData);
            console.log("APP ID:", tokenData.appId);
            console.log("TOKEN:", tokenData.token);
            console.log("CHANNEL:", tokenData.channel);
            console.log("UID:", tokenData.uid);    


            // Join Agora.

            await joinAgoraRoom({
                appId:
                    tokenData.appId,

                token:
                    tokenData.token,

                channel:
                    tokenData.channel,

                uid:
                    generatedUid
            });


            setJoined(true);

            setStatus(
                "Connected"
            );

        } catch (error) {

            console.error(error);

            setStatus(
                "Connection failed"
            );

            alert(error.message);
        }
    }


    async function handleStartAgent() {

        try {

            setStatus(
                "Starting AI agent..."
            );

            const response =
                await startAgent(
                    incidentId,
                    incidentId
                );

            console.log(
                "Agent response:",
                response
            );

            setAgentStarted(true);

            setStatus(
                "AI Incident Commander listening"
            );

        } catch (error) {

            console.error(error);

            setStatus(
                "Agent failed to start"
            );

            alert(error.message);
        }
    }


    function handleMute() {

        const nextMuted =
            !muted;

        setMuted(
            nextMuted
        );

        setMutedState(
            nextMuted
        );
    }


    async function handleLeave() {

        await leaveAgoraRoom();

        setJoined(false);

        setAgentStarted(false);

        setStatus(
            "Disconnected"
        );
    }


    return (

        <div className="container">

            <div className="card">

                <h1>
                    Agora Incident Commander
                </h1>

                <p className="subtitle">
                    Join a live incident room and connect
                    the AI Incident Commander.
                </p>


                {!joined ? (

                    <>
                        <div className="form-group">

                            <label>
                                Your Name
                            </label>

                            <input
                                type="text"
                                value={name}
                                onChange={
                                    (event) =>
                                        setName(
                                            event.target.value
                                        )
                                }
                                placeholder="Enter your name"
                            />

                        </div>


                        <div className="form-group">

                            <label>
                                Role
                            </label>

                            <select
                                value={role}
                                onChange={
                                    (event) =>
                                        setRole(
                                            event.target.value
                                        )
                                }
                            >

                                <option value="incident-commander">
                                    Incident Commander
                                </option>

                                <option value="on-call-sre">
                                    On-call SRE
                                </option>

                                <option value="backend-engineer">
                                    Backend Engineer
                                </option>

                                <option value="support-lead">
                                    Support Lead
                                </option>

                                <option value="engineering-manager">
                                    Engineering Manager
                                </option>

                            </select>

                        </div>


                        <div className="form-group">

                            <label>
                                Team
                            </label>

                            <input
                                type="text"
                                value={team}
                                onChange={
                                    (event) =>
                                        setTeam(
                                            event.target.value
                                        )
                                }
                                placeholder="payments"
                            />

                        </div>


                        <div className="form-group">

                            <label>
                                Incident ID
                            </label>

                            <input
                                type="text"
                                value={incidentId}
                                onChange={
                                    (event) =>
                                        setIncidentId(
                                            event.target.value
                                        )
                                }
                                placeholder="incident-4821"
                            />

                        </div>


                        <button
                            className="primary-button"
                            onClick={handleJoin}
                        >
                            Join Incident Room
                        </button>
                    </>

                ) : (

                    <>
                        <div className="incident-info">

                            <div>
                                <strong>
                                    Incident
                                </strong>

                                <span>
                                    {incidentId}
                                </span>
                            </div>


                            <div>
                                <strong>
                                    Participant
                                </strong>

                                <span>
                                    {name}
                                </span>
                            </div>


                            <div>
                                <strong>
                                    Role
                                </strong>

                                <span>
                                    {role}
                                </span>
                            </div>


                            <div>
                                <strong>
                                    UID
                                </strong>

                                <span>
                                    {uid}
                                </span>
                            </div>

                        </div>


                        <div className="status-box">

                            <span
                                className={
                                    joined
                                        ? "status-dot connected"
                                        : "status-dot"
                                }
                            />

                            <span>
                                {status}
                            </span>

                        </div>


                        <div className="controls">

                            <button
                                className="secondary-button"
                                onClick={handleMute}
                            >
                                {
                                    muted
                                        ? "Unmute Microphone"
                                        : "Mute Microphone"
                                }
                            </button>


                            {!agentStarted ? (

                                <button
                                    className="agent-button"
                                    onClick={
                                        handleStartAgent
                                    }
                                >
                                    Start AI Commander
                                </button>

                            ) : (

                                <button
                                    className="agent-button"
                                    disabled
                                >
                                    AI Commander Active
                                </button>

                            )}


                            <button
                                className="danger-button"
                                onClick={handleLeave}
                            >
                                Leave Incident
                            </button>

                        </div>


                        <div className="agent-panel">

                            <h2>
                                AI Incident Commander
                            </h2>

                            {
                                agentStarted ? (

                                    <p>
                                        AI agent is connected and
                                        listening to the incident room.
                                    </p>

                                ) : (

                                    <p>
                                        Start the AI agent after
                                        joining the incident room.
                                    </p>

                                )
                            }

                        </div>

                    </>

                )}

            </div>

        </div>
    );
}