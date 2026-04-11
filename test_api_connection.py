import requests
import os
import wave

from config import settings

BASE_URL = settings.TEST_URL
endpoint = f"{BASE_URL}/inference_zero_shot"

with open("test_files/barney_prompt_01.txt", "r") as f:
    prompt_text = f.read()

payload = {
    "tts_text": "This is how I met your mother.",
    "prompt_text": "You are a helpful assistant.<|endofprompt|>" + prompt_text,
}
files = [
    (
        "prompt_wav",
        (
            "prompt_wav",
            open("test_files/barney_prompt_01.wav", "rb"),
            "application/octet-stream",
        ),
    )
]
response = requests.request("GET", endpoint, data=payload, files=files, stream=True)


output_file = "output.wav"
if response.status_code == 200:
    audio_data = b""
    for chunk in response.iter_content(chunk_size=16000):
        audio_data += chunk
    sample_rate = 24000
    channels = 1
    sample_width = 2

    with wave.open(output_file, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data)
