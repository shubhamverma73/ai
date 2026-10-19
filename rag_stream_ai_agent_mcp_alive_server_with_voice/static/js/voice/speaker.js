

function speak(text) {

    if (!text.trim()) return;

    VoiceState.speechQueue.push(text);

    playNextSentence();
}


function playNextSentence() {

    if (VoiceState.isSpeaking) return;

    if (VoiceState.speechQueue.length === 0) return;

    VoiceState.isSpeaking = true;

    const utterance = new SpeechSynthesisUtterance(
        VoiceState.speechQueue.shift()
    );

    utterance.rate = 1;

    utterance.pitch = 1;

    utterance.volume = 1;

    utterance.onend = () => {

        VoiceState.isSpeaking = false;

        playNextSentence();

        // Queue khatam?
        if (
            VoiceState.voiceMode &&
            VoiceState.waitForNextRecording &&
            VoiceState.speechQueue.length === 0
        ) {

            VoiceState.waitForNextRecording = false;

            setTimeout(async () => {

                if (
                    !VoiceState.isRecording &&
                    !VoiceState.isSpeaking
                ) {

                    await startRecording();

                }

            }, VoiceState.autoRestartDelay);

        }

    };

    speechSynthesis.speak(utterance);

}

// ------------------------- Helper -------------
function stopSpeaking() {

    // Browser TTS stop
    speechSynthesis.cancel();

    // Queue clear
    VoiceState.speechQueue = [];

    // Reset state
    VoiceState.isSpeaking = false;

    // Pending sentence bhi clear
    VoiceState.sentenceBuffer = "";

    console.log("Speech Stopped");

}