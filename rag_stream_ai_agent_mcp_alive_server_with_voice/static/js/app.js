console.log("=====================>", VoiceState);

async function sendQuestion() {

    const input =
        document.getElementById(
            "question"
        );

    const question =
        input.value;

    if (!question.trim()) return;

    input.value = "";

    const sendBtn =
        document.querySelector(
            "button"
        );

    sendBtn.disabled = true;

    const chatBox =
        document.getElementById(
            "chat-box"
        );

    chatBox.innerHTML +=
        `<p><b>You:</b> ${question}</p>`;

    const botMessage =
        document.createElement("p");

    botMessage.innerHTML =
        `
    <b>Bot:</b>
    <span class="loading">
        🔍 Searching documents...
    </span>
    `;

    const loadingMessages = [
        "🔍 Searching documents...",
        "📄 Reading PDF content...",
        "🧠 Analyzing context...",
        "✍️ Generating answer..."
    ];

    let loadingIndex = 0;

    const loadingInterval =
        setInterval(() => {

            loadingIndex =
                (loadingIndex + 1)
                % loadingMessages.length;

            botMessage.innerHTML =
                `
            <b>Bot:</b>
            <span class="loading">
                ${loadingMessages[
                loadingIndex
                ]}
            </span>
            `;
        }, 1500);

    chatBox.appendChild(
        botMessage
    );

    const response = await fetch(
        "/chat",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                question
            })
        }
    );

    const reader =
        response.body.getReader();

    const decoder =
        new TextDecoder();

    let answer = "";

    while (true) {

        const {
            value,
            done
        } = await reader.read();

        if (done) break;

        const chunk =
            decoder.decode(value);

        clearInterval(
            loadingInterval
        );

        sendBtn.disabled = false;

        if (
            chunk.includes(
                "__END_STREAM__"
            )
        ) {

            answer += chunk.replace(
                "__END_STREAM__",
                ""
            );

            VoiceState.waitForNextRecording = true;

            break;
        }

        answer += chunk;

        botMessage.innerHTML =
            `<b>Bot:</b><br>` +
            marked.parse(answer);

        VoiceState.sentenceBuffer += chunk;

        const sentences = VoiceState.sentenceBuffer.split(/(?<=[.!?])/);

        while (sentences.length > 1) {

            const sentence = sentences.shift().trim();

            if (sentence.length > 0) {

                speak(sentence);

            }

        }

        VoiceState.sentenceBuffer = sentences[0];

        chatBox.scrollTop =
            chatBox.scrollHeight;

        // AI bolega
        // speak(answer);
    }

    const sourceResponse =
        await fetch("/sources");

    const sources =
        await sourceResponse.json();

    let sourcesHtml = "";

    if (sources.length > 0) {

        sourcesHtml =
            "<br><br><b>Sources:</b><br>";

        sources.forEach(source => {

            sourcesHtml += `
            <div class="source-item">
                📄 ${source.source}
                <small>
                    (Page ${source.page})
                </small>
            </div>
            `;
        });
    }

    botMessage.innerHTML =
        `<b>Bot:</b><br>` +
        marked.parse(answer) +
        sourcesHtml;

    if (VoiceState.sentenceBuffer.trim()) {

        speak(VoiceState.sentenceBuffer);

        VoiceState.sentenceBuffer = "";

    }

    chatBox.scrollTop =
        chatBox.scrollHeight;
}

// ===================================================================
const micButton = document.getElementById("mic-btn");

micButton.addEventListener("click", async () => {

    if (!VoiceState.isRecording) {

        VoiceState.voiceMode = true;

        await startRecording();

        micButton.innerHTML = "⏹️";
        micButton.style.background = "red";

    } else {

        VoiceState.voiceMode = false;

        await stopRecording();

        micButton.innerHTML = "🎤";
        micButton.style.background = "";

    }

});

/*micButton.addEventListener("click", async () => {

    // Agar AI bol raha hai to pehle usse chup karao
    stopSpeaking();

    // -------------------------
    // START RECORDING
    // -------------------------
    if (!VoiceState.isRecording) {

        VoiceState.stream = await navigator.mediaDevices.getUserMedia({
            audio: true
        });

        VoiceState.mediaRecorder = new MediaRecorder(VoiceState.stream);

        VoiceState.audioChunks = [];

        VoiceState.mediaRecorder.ondataavailable = (event) => {
            VoiceState.audioChunks.push(event.data);
        };

        VoiceState.mediaRecorder.onstop = async () => {

            const audioBlob = new Blob(VoiceState.audioChunks, {
                type: "audio/webm"
            });

            const formData = new FormData();

            formData.append(
                "audio",
                audioBlob,
                "voice.webm"
            );

            const response = await fetch(
                "/transcribe",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();

            document.getElementById(
                "question"
            ).value = data.text;

            sendQuestion();

        };

        VoiceState.mediaRecorder.start();

        VoiceState.isRecording = true;

        micButton.innerHTML = "⏹️";
        micButton.style.background = "red";

        console.log("Recording Started");

        return;

    }

    // -------------------------
    // STOP RECORDING
    // -------------------------

    VoiceState.mediaRecorder.stop();

    VoiceState.stream.getTracks().forEach(track => track.stop());

    VoiceState.isRecording = false;

    micButton.innerHTML = "🎤";
    micButton.style.background = "";

    console.log("Recording Stopped");

});*/