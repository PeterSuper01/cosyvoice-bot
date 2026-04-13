import asyncio
import discord
from discord.ext import commands
import re
import emoji


class TTSCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._queue = asyncio.Queue()
        self._task = None

    def _clean_text(self, text):
        text = re.sub(r"<a?:\w+:\d+>", "", text)
        text = emoji.replace_emoji(text, replace="")
        return text.strip()

    def _get_vc(self):
        return self.bot.voice_clients[0] if self.bot.voice_clients else None

    async def _player_loop(self, vc):
        while True:
            try:
                audio = await asyncio.wait_for(self._queue.get(), timeout=300)
            except asyncio.TimeoutError:
                break
            audio.seek(0)
            vc.play(discord.FFmpegPCMAudio(audio, pipe=True, before_options="-f wav"))
            while vc.is_playing():
                await asyncio.sleep(0.1)
            self._queue.task_done()

    async def _enqueue(self, ctx, audio):
        vc = self._get_vc()
        if vc is None:
            await ctx.reply("Bot is not in the voice channel.")
            return
        await self._queue.put(audio)
        if self._task is None or self._task.done():
            self._task = self.bot.loop.create_task(self._player_loop(vc))

    @commands.command()
    async def register(self, ctx: commands.Context, *, prompt_text: str = ""):
        if not ctx.message.attachments:
            await ctx.reply("Attach a .wav file.")
            return
        wav_bytes = await ctx.message.attachments[0].read()
        result = await self.bot.tts_client.save_speaker(
            str(ctx.author.id), prompt_text, wav_bytes
        )
        await ctx.reply(
            f"Registered! {result.get('recognized_prompt_text', '')}"
            if result["success"]
            else f"Failed: {result['error']}"
        )

    @commands.command()
    async def tts(self, ctx: commands.Context, *, text):
        clean_text = self._clean_text(text)
        if not clean_text:
            await ctx.reply("No text left after cleaning emojis.")
            return
        result = await self.bot.tts_client.get_speech(str(ctx.author.id), clean_text)
        if not result["success"]:
            await ctx.reply(f"Failed: {result['error']}")
            return
        await self._enqueue(ctx, result["audio"])
        await ctx.message.add_reaction("🔊")


async def setup(bot):
    await bot.add_cog(TTSCog(bot))
