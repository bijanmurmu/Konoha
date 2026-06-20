import discord
from discord.ext import commands
from discord import app_commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ping', description='Check if the bot is alive.')
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f'Pong! 🏓 My latency is {latency}ms')

    @app_commands.command(name='hello', description='Say hello to the bot.')
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Hello there, {interaction.user.mention}! Welcome to Konoha.')

async def setup(bot):
    await bot.add_cog(General(bot))
