import discord
from discord.ext import commands
from openai import ChatCompletion

class ChatGPTCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("/gpt3")
    async def chat(self, ctx, *, message):
        # Construct the chat message payload
        messages = [
            {"role": "system", "content": "You are chatting with GPT-3.5-turbo"},
            {"role": "user", "content": message},
        ]

        # Make the OpenAI API call
        response = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Extract the assistant's reply
        gpt_reply = response['choices'][0]['message']['content']
        await ctx.send(gpt_reply)

def setup(bot):
    bot.add_cog(ChatGPTCog(bot))
