from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, name: str):
        try:
            await self.bot.load_extension(f"cogs.{name}")
            await ctx.send(f"Loaded {name}!")
        except Exception as e:
            await ctx.send(f"Error loading extension '{name}':\n```py\n{e}\n```")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, name: str):
        try:
            await self.bot.reload_extension(f"cogs.{name}")
            await ctx.send(f"Extension '{name}' reloaded successfully.")
        except Exception as e:
            await ctx.send(f"Failed to reload extension '{name}':\n```py\n{e}\n```")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, name: str):
        try:
            await self.bot.unload_extension(f"cogs.{name}")
            await ctx.send(f"Extension '{name}' has been unloaded successfully.")
        except Exception as e:
            await ctx.send(f"Error unloading extension '{name}':\n```py\n{e}\n```")

    @commands.command()
    @commands.is_owner()
    async def logout(self, ctx):
        try:
            await ctx.send("Bot is shutting down...")
            await self.bot.close()
        except Exception as e:
            await ctx.send(f"Error during shutdown:\n```py\n{e}\n```")


async def setup(bot):
    await bot.add_cog(Admin(bot))
