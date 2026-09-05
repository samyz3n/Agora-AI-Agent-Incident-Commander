const API_URL =
    import.meta.env.VITE_API_URL;

console.log("API URL =",API_URL);


export async function getAgoraToken(
    channel,
    uid
) {

    const response = await fetch(
        `${API_URL}/api/agora/token`,
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                channel,
                uid
            })
        }
    );

    if (!response.ok) {
        throw new Error(
            await response.text()
        );
    }

    const data = await response.json();

    console.log("TOKEN API RESPONSE:", data);

    return data;
}


export async function registerParticipant(
    incidentId,
    participant
) {

    const response = await fetch(
        `${API_URL}/api/incidents/` +
        `${incidentId}/participants`,
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body:
                JSON.stringify(
                    participant
                )
        }
    );

    if (!response.ok) {
        throw new Error(
            await response.text()
        );
    }

    return response.json();
}


export async function startAgent(
    incidentId,
    channel
) {

    const response = await fetch(
        `${API_URL}/api/incidents/` +
        `${incidentId}/start-agent`,
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                channel
            })
        }
    );

    if (!response.ok) {

        const error =
            await response.text();

        throw new Error(error);
    }

    return response.json();
}