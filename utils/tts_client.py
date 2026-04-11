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
