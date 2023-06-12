import discord
from discord.ext import commands

class CommunityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_balance = {}  # This would ideally be a database in a real bot

    @commands.command("/poll")
    async def create_poll(self, ctx, question: str, *options: str):
        if len(options) < 2:
            await ctx.send("A poll must have at least two options.")
            return
        if len(options) > 10:
            await ctx.send("A poll cannot have more than 10 options.")
            return

        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(title=question, description=''.join(description))

        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)

    @commands.command("/tip")
    async def tip(self, ctx, recipient: discord.Member, amount: int):
        sender_id = str(ctx.message.author.id)
        recipient_id = str(recipient.id)
        if sender_id not in self.user_balance or self.user_balance[sender_id] < amount:
            await ctx.send("You don't have enough Audacity Dollars to tip that amount.")
            return

        self.user_balance[sender_id] -= amount
        if recipient_id not in self.user_balance:
            self.user_balance[recipient_id] = 0
        self.user_balance[recipient_id] += amount
        await ctx.send(f"{ctx.message.author.name} tipped {recipient.name} ${amount} Audacity Dollars!")

def setup(bot):
    bot.add_cog(CommunityCog(bot))
