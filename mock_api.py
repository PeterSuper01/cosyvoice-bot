import uvicorn
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def generate_dummy():
    for _ in range(10):
        yield b"\x00" * 16000


@app.api_route("/inference_zero_shot", methods=["GET", "POST"])
async def inference_zero_shot(
    tts_text: str = Form(...),
    prompt_text: str = Form(...),
    prompt_wav: UploadFile = File(...),
):
    return StreamingResponse(generate_dummy(), media_type="audio/wav")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=50000)
