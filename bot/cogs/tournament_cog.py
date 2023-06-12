import discord
from discord.ext import commands

class TournamentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tournaments = []

    @commands.command()
    @commands.has_role("Admin")  # Only allow admins to use this command
    async def create_tournament(self, ctx, name: str):
        tournament = {
            "name": name,
            "teams": []
        }
        self.tournaments.append(tournament)
        await ctx.send(f"Tournament '{name}' has been created!")

    @commands.command()
    @commands.has_role("Admin")  # Only allow admins to use this command
    async def add_team(self, ctx, tournament_name: str, team_name: str):
        for tournament in self.tournaments:
            if tournament['name'] == tournament_name:
                team = {
                    "name": team_name,
                    "members": [],
                    "stats": {"wins": 0, "losses": 0}
                }
                tournament['teams'].append(team)
                await ctx.send(f"Team '{team_name}' has been added to tournament '{tournament_name}'!")
                return
        await ctx.send(f"Tournament '{tournament_name}' not found.")

    @commands.command()
    @commands.has_role("Admin")  # Only allow admins to use this command
    async def add_member(self, ctx, tournament_name: str, team_name: str, member_name: str):
        for tournament in self.tournaments:
            if tournament['name'] == tournament_name:
                for team in tournament['teams']:
                    if team['name'] == team_name:
                        team['members'].append(member_name)
                        await ctx.send(f"Member '{member_name}' has been added to team '{team_name}' in tournament '{tournament_name}'!")
                        return
        await ctx.send(f"Team '{team_name}' not found in tournament '{tournament_name}'.")

    @commands.command()
    async def view_tournament(self, ctx, tournament_name: str):
        for tournament in self.tournaments:
            if tournament['name'] == tournament_name:
                response = f"Tournament '{tournament['name']}':\n"
                for team in tournament['teams']:
                    response += f"Team '{team['name']}':\n"
                    response += f"Members: {', '.join(team['members'])}\n"
                    response += f"Wins: {team['stats']['wins']}, Losses: {team['stats']['losses']}\n"
                await ctx.send(response)
                return
        await ctx.send(f"Tournament '{tournament_name}' not found.")

def setup(bot):
    bot.add_cog(TournamentCog(bot))
