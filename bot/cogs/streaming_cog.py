import discord
from discord.ext import commands

class StreamingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("/stream")
    @commands.has_role("Admin")  # Only allow admins to use this command
    async def share_stream(self, ctx, stream_name: str, stream_link: str):
        await ctx.send(f"{stream_name} is now live! Watch here: {stream_link}")

def setup(bot):
    bot.add_cog(StreamingCog(bot))