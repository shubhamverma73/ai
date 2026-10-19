const VoiceState = {

    isRecording: false,

    isSpeaking: false,

    voiceMode: false,

    waitForNextRecording: false,

    autoRestartDelay: 500,

    mediaRecorder: null,

    stream: null,

    audioChunks: [],

    speechQueue: [],

    sentenceBuffer: "",

    audioContext: null,

    analyser: null,

    silenceTimer: null,

    silenceThreshold: 8,

    silenceDuration: 2000,

    vadRunning: false,

};