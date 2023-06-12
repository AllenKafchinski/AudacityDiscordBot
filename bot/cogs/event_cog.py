import discord
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from discord.ext import commands

class EventCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.events = []

    @commands.command("/NewEvent")
    @commands.has_role("Admin")  # Only allow admins to use this command
    async def add_event(self, ctx, title: str, date: str, time: str, duration: str):
        event = {
            "title": title,
            "date": date,
            "time": time,
            "duration": duration,
        }
        self.events.append(event)
        await ctx.send(f"Event '{title}' has been added!")

    @commands.command("/Events")
    async def list_events(self, ctx):
        if not self.events:
            await ctx.send("No events scheduled.")
            return

        for event in self.events:
            await ctx.send(f"Title: {event['title']}\nDate: {event['date']}\nTime: {event['time']}\nDuration: {event['duration']}")

def setup(bot):
    bot.add_cog(EventCog(bot))
