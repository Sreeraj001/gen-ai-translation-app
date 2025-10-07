from gtts import gTTS
from io import BytesIO

#Converts text to speech and returns audio bytes
def text_to_speech(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes
    except Exception as e:
        raise RuntimeError(f"Text-to-speech conversion failed: {e}")