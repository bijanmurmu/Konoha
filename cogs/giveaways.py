import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random

class Giveaways(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='giveaway_start', description='Start a server giveaway.')
    @app_commands.checks.has_permissions(manage_events=True)
    async def giveaway_start(self, interaction: discord.Interaction, duration_seconds: int, prize: str, winners: int = 1):
        embed = discord.Embed(
            title="🎉 NETWORK REWARD INITIATED",
            description=f"**Prize:** {prize}\n**Winners:** {winners}\n**Duration:** {duration_seconds} seconds\n\n> REACT WITH 🎉 TO ENTER.",
            color=0xff1e1e
        )
        embed.set_footer(text="Konoha Reward System")
        
        await interaction.response.send_message("> GIVERAWAY INITIATED.", ephemeral=True)
        msg = await interaction.channel.send(embed=embed)
        await msg.add_reaction("🎉")
        
        # Wait for duration
        await asyncio.sleep(duration_seconds)
        
        # Fetch updated message to get reactions
        new_msg = await interaction.channel.fetch_message(msg.id)
        
        users = []
        for reaction in new_msg.reactions:
            if reaction.emoji == "🎉":
                async for user in reaction.users():
                    if not user.bot:
                        users.append(user)
                        
        if len(users) == 0:
            await interaction.channel.send("> ERROR: NO VALID ENTRIES DETECTED. GIVERAWAY CANCELLED.")
            return
            
        winners_list = random.sample(users, min(winners, len(users)))
        mentions = ", ".join([w.mention for w in winners_list])
        
        win_embed = discord.Embed(
            title="🎉 GIVEAWAY CONCLUDED",
            description=f"**Prize:** {prize}\n**Winners:** {mentions}",
            color=0x00ff00
        )
        await interaction.channel.send(content=f"Congratulations {mentions}!", embed=win_embed)

async def setup(bot):
    await bot.add_cog(Giveaways(bot))
