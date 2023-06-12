import discord
from discord.ext import commands

class VRChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vrchat_events = []

    @commands.command("/vrchatAddevent")
    @commands.has_role("Admin")  # Only allow admins to use this command
    async def create_vrchat_event(self, ctx, event_name: str, world_link: str, user_link: str):
        vrchat_event = {
            "event_name": event_name,
            "world_link": world_link,
            "user_link": user_link,
        }
        self.vrchat_events.append(vrchat_event)
        await ctx.send(f"VRChat event '{event_name}' has been created!")

    @commands.command("/vrchat")
    async def list_vrchat_events(self, ctx):
        if not self.vrchat_events:
            await ctx.send("No VRChat events scheduled.")
            return

        for event in self.vrchat_events:
            await ctx.send(f"Event Name: {event['event_name']}\nWorld Link: {event['world_link']}\nHosted by: {event['user_link']}")

def setup(bot):
    bot.add_cog(VRChatCog(bot))