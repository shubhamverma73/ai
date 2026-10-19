
async function startRecording() {

    stopSpeaking();

    VoiceState.stream = await navigator.mediaDevices.getUserMedia({
        audio: true
    });

    VoiceState.mediaRecorder = new MediaRecorder(VoiceState.stream);

    VoiceState.audioChunks = [];

    VoiceState.mediaRecorder.ondataavailable = (event) => {
        VoiceState.audioChunks.push(event.data);
    };

    VoiceState.mediaRecorder.onstop = async () => {

        console.log("onstop fired");

        const audioBlob = new Blob(VoiceState.audioChunks, {
            type: "audio/webm"
        });

        const formData = new FormData();

        formData.append(
            "audio",
            audioBlob,
            "voice.webm"
        );

        console.log("Uploading audio...");

        const response = await fetch("/transcribe", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        console.log(data);

        document.getElementById("question").value = data.text;

        sendQuestion();

    };

    VoiceState.mediaRecorder.start();

    // Voice Activity Detection Start
    startSilenceDetection();

    VoiceState.isRecording = true;

    console.log("Recording Started");

}

async function stopRecording() {

    console.log("stopRecording() called");

    VoiceState.vadRunning = false;

    VoiceState.mediaRecorder.stop();

    VoiceState.stream.getTracks().forEach(track => track.stop());

    if (VoiceState.audioContext) {

        VoiceState.audioContext.close();

        VoiceState.audioContext = null;

    }

    if (VoiceState.silenceTimer) {

        clearTimeout(
            VoiceState.silenceTimer
        );

        VoiceState.silenceTimer = null;

    }

    VoiceState.isRecording = false;

    console.log("Recording Stopped");
    console.log("stopRecording() finished");

}

async function startSilenceDetection() {

    VoiceState.vadRunning = true;

    VoiceState.audioContext =
        new AudioContext();

    const source =
        VoiceState.audioContext
            .createMediaStreamSource(
                VoiceState.stream
            );

    VoiceState.analyser =
        VoiceState.audioContext
            .createAnalyser();

    VoiceState.analyser.fftSize = 512;

    source.connect(
        VoiceState.analyser
    );

    const data =
        new Uint8Array(
            VoiceState.analyser.frequencyBinCount
        );

    detectSilence(data);

}

function detectSilence(data) {

    if (!VoiceState.vadRunning) {

        return;

    }

    VoiceState.analyser.getByteFrequencyData(data);

    let volume = 0;

    for (let i = 0; i < data.length; i++) {

        volume += data[i];

    }

    volume /= data.length;

    console.log(volume);

    if (volume > VoiceState.silenceThreshold) {

        // User bol raha hai

        if (VoiceState.silenceTimer) {

            clearTimeout(
                VoiceState.silenceTimer
            );

            VoiceState.silenceTimer = null;

        }

    } else {

        // User chup hai

        if (!VoiceState.silenceTimer) {

            VoiceState.silenceTimer =
                setTimeout(async () => {

                    console.log(
                        "Silence Detected"
                    );

                    if (
                        VoiceState.isRecording
                    ) {

                        await stopRecording();

                    }

                }, VoiceState.silenceDuration);

        }

    }

    requestAnimationFrame(() =>
        detectSilence(data)
    );

}