import discord
import asyncio
from discord.ext import commands, tasks
from datetime import datetime, timedelta

class EventCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.events = []
        self.notification_channel_id = None  # Initialize the notification_channel_id attribute
        self.post_todays_events.start()  # Start the daily loop

    @commands.command("/NewEvent")
    @commands.has_role("Admin")  # Only allow admins to use this command
    async def add_event(self, ctx, title: str, date: str, time: str, duration: str):
        event_id = len(self.events) + 1
        event = {
            "id": event_id,
            "title": title,
            "date": date,
            "time": time,
            "duration": duration,
        }
        self.events.append(event)
        await ctx.send(f"Event '{title}' has been added!")

    @commands.command("/EditEvent")
    @commands.has_role("Admin")
    async def edit_event(self, ctx, event_id: int, field: str, value: str):
        for event in self.events:
            if event["id"] == event_id:
                event[field] = value
                await ctx.send(f"Event {event_id} '{field}' has been updated to '{value}'.")
                return
        await ctx.send("Event not found.")

    @commands.command("/Events")
    async def list_events(self, ctx):
        if not self.events:
            await ctx.send("No events scheduled.")
            return

        for event in self.events:
            await ctx.send(f"ID: {event['id']}\nTitle: {event['title']}\nDate: {event['date']}\nTime: {event['time']}\nDuration: {event['duration']}")

    @commands.command("/SetNotificationChannel")
    @commands.has_role("Admin")
    async def set_notification_channel(self, ctx, channel_id: int):
        self.notification_channel_id = channel_id
        await ctx.send(f"Notification channel has been set to: {channel_id}")

    @tasks.loop(hours=24)  # Loop every 24 hours
    async def post_todays_events(self):
        if self.notification_channel_id is None:
            return  # Do nothing if the notification_channel_id has not been set
    
        today = datetime.now().strftime('%Y-%m-%d')
        channel = self.bot.get_channel(self.notification_channel_id)
        
        for event in self.events:
            if event["date"] == today:
                await channel.send(f"**Today's Event:**\n```Title: {event['title']}\nDate: {event['date']}\nTime: {event['time']}\nDuration: {event['duration']}```")
    

    @post_todays_events.before_loop
    async def before_post_todays_events(self):
        now = datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        delta = midnight - now
        await asyncio.sleep(delta.total_seconds())  # Sleep until midnight before starting the loop

def setup(bot):
    bot.add_cog(EventCog(bot))
