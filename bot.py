from discord.ext import commands
import discord

from utils.tts_client import TTSClient

intents = discord.Intents.default()
intents.message_content = True


class TTSBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.tts_client = TTSClient()

    async def close(self):
        await self.tts_client.close()
        await super().close()
