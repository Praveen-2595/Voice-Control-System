import whisper
import tempfile
import wave

model = whisper.load_model("small")

def recognize(audio):
    if not audio:
        return ""

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        wf = wave.open(f.name, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio)
        wf.close()

        result = model.transcribe(f.name, language="en")

        text = result["text"].lower().strip()

# ignore garbage
        if len(text.split()) < 2:
            return ""

        return text

    return result["text"].lower().strip()