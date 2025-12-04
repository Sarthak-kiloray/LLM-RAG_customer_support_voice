# tts_agent.py
from openai import OpenAI

client = OpenAI()

OPENAI_TTS_VOICES = [
    "alloy", "ash", "ballad", "coral", "echo", "fable",
    "onyx", "nova", "sage", "shimmer", "verse",
]


def synthesize_speech(text: str, voice: str = "nova") -> bytes:
    """
    Returns raw MP3 audio bytes from OpenAI TTS.
    """
    if voice not in OPENAI_TTS_VOICES:
        voice = "nova"

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",  # or gpt-4o-tts if you have access
        voice=voice,
        input=text,
        response_format="mp3",    # ✅ correct parameter name
    )

    audio_bytes = response.read()
    return audio_bytes
