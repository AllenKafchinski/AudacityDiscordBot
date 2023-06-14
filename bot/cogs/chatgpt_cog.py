import os
import discord
from discord.ext import commands
from openai import ChatCompletion
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_KEY")
temp = float(os.getenv("OPENAI_TEMP", 1))
max_tokens = int(os.getenv("MAX_TOKENS", 1000))

# Set up OpenAI API
ChatCompletion.api_key = openai_api_key

class ChatGPTCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("/gpt")
    async def chat(self, ctx, model_version: str, *, message):
        # Pre-prompt for Discord bot formatting
        pre_prompt = "You are a helpful Discord bot. Format your responses accordingly for Discord."

        # Choose the appropriate model based on user input
        if model_version.lower() == "gpt3.5":
            model = "gpt-3.5-turbo"
        elif model_version.lower() == "gpt4":
            model = "gpt-4" 
        else:
            await ctx.send("Invalid model version. Please choose either 'gpt3.5' or 'gpt4'.")
            return

        # Construct the chat message payload
        messages = [
            {"role": "system", "content": f"{pre_prompt}\n\nYou are chatting with {model}"},
            {"role": "user", "content": message},
        ]

        # Make the OpenAI API call
        response = ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temp,
            max_tokens=max_tokens
        )

        # Extract the assistant's reply
        gpt_reply = response['choices'][0]['message']['content']
        await ctx.send(gpt_reply)

def setup(bot):
    bot.add_cog(ChatGPTCog(bot))
