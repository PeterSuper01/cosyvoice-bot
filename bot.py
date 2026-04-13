import asyncio
from discord.ext import commands
import discord

from config import settings
from utils.tts_client import TTSClient

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True


class TTSBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.tts_client = TTSClient()
        self.discord_voice_channel_id = settings.DISCORD_VOICE_CHANNEL_ID

    async def setup_hook(self):
        await self.load_extension("cogs.tts")

    async def on_ready(self):
        channel = self.get_channel(int(self.discord_voice_channel_id))
        await channel.connect()

    async def close(self):
        for vc in self.voice_clients:
            await vc.disconnect(force=True)
        await self.tts_client.close()
        await super().close()


async def main():
    bot = TTSBot()
    async with bot:
        await bot.start(settings.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
