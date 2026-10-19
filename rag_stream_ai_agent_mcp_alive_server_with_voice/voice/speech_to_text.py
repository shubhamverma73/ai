from faster_whisper import WhisperModel

# Model sirf ek baar load hoga
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

def transcribe_audio(audio_path):

    segments, info = model.transcribe(audio_path)

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()