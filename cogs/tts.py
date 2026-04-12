import discord
from discord.ext import commands


class TTSCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx: commands.Context, *, prompt_text: str):
        if not ctx.message.attachments:
            await ctx.reply("Attach a .wav file.")
            return
        wav_bytes = await ctx.message.attachments[0].read()
        result = await self.bot.tts_client.save_speaker(
            str(ctx.author.id), prompt_text, wav_bytes
        )
        await ctx.reply(
            "Registered!" if result["success"] else f"Failed: {result['error']}"
        )


async def setup(bot):
    await bot.add_cog(TTSCog(bot))
