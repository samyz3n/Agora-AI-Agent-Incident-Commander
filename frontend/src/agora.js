import AgoraRTC from "agora-rtc-sdk-ng";


export const agoraClient =
    AgoraRTC.createClient({
        mode: "rtc",
        codec: "vp8"
    });


let microphoneTrack = null;


export async function joinAgoraRoom({
    appId,
    token,
    channel,
    uid
}) {
    console.log("appId:",appId);
    console.log("token:",token);
    console.log("channel",channel);
    console.log("uid:",uid);
    await agoraClient.join(
        appId,
        channel,
        token,
        uid
    );

    microphoneTrack =
        await AgoraRTC
            .createMicrophoneAudioTrack();

    await agoraClient.publish(
        microphoneTrack
    );

    console.log(
        "Joined Agora channel:",
        channel
    );

    return microphoneTrack;
}


export function setupRemoteAudio() {

    agoraClient.on(
        "user-published",

        async (
            user,
            mediaType
        ) => {

            await agoraClient.subscribe(
                user,
                mediaType
            );

            console.log(
                "Subscribed to:",
                user.uid,
                mediaType
            );

            if (
                mediaType === "audio"
            ) {

                user.audioTrack.play();
            }
        }
    );


    agoraClient.on(
        "user-unpublished",

        (
            user,
            mediaType
        ) => {

            console.log(
                "User unpublished:",
                user.uid,
                mediaType
            );
        }
    );


    agoraClient.on(
        "user-left",

        user => {

            console.log(
                "User left:",
                user.uid
            );
        }
    );
}


export function setMuted(
    muted
) {

    if (!microphoneTrack) {
        return;
    }

    microphoneTrack.setMuted(
        muted
    );
}


export async function leaveAgoraRoom() {

    if (microphoneTrack) {

        microphoneTrack.stop();

        microphoneTrack.close();

        microphoneTrack = null;
    }

    await agoraClient.leave();
}