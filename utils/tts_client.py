import asyncio
import io
from typing import Optional

import aiohttp


class TTSClient:
    def __init__(self, port=50000):
        self.base_url = f"http://127.0.0.1:{port}"
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def save_speaker(
        self, spk_id: str, prompt_text: str, wav_bytes: bytes
    ) -> dict:
        session = await self._get_session()

        data = aiohttp.FormData()
        data.add_field("spk_id", spk_id)
        data.add_field(
            "prompt_text", "You are a helpful assistant.<|endofprompt|>" + prompt_text
        )
        data.add_field(
            "prompt_wav",
            wav_bytes,
            filename=f"{spk_id}_prompt.wav",
            content_type="audio/wav",
        )

        try:
            async with session.post(
                f"{self.base_url}/save_speaker", data=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return {"success": result["success"], "spk_id": result["spk_id"]}
                else:
                    error_detail = await response.text()
                    return {
                        "success": False,
                        "error": f"API Error {response.status}: {error_detail}",
                    }
        except Exception as e:
            return {"success": False, "error": f"Connection Exception: {str(e)}"}

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
