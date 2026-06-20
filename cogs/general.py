import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ping', description='Check system latency.')
    async def ping(self, interaction: discord.Interaction):
        latency_ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(f'> CONNECTION SECURE. LATENCY {latency_ms}MS.')

    @app_commands.command(name='scan', description='Run a network threat scan.')
    async def scan(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="SYSTEM SCAN COMPLETE",
            description=f"**Threats Found:** 0\n**Network Status:** SECURE\n**Latency:** {round(self.bot.latency * 1000)}ms",
            color=0xff1e1e
        )
        embed.set_footer(text="KONOHA NETWORK SCANNER")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='profile', description='View your complete network profile.')
    async def profile(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        
        # Load data
        wallet, bank, level, xp = 0, 0, 0, 0
        
        if os.path.exists('economy_data.json'):
            with open('economy_data.json', 'r') as f:
                eco_data = json.load(f)
                if str(member.id) in eco_data:
                    wallet = eco_data[str(member.id)].get('wallet', 0)
                    bank = eco_data[str(member.id)].get('bank', 0)
                    
        if os.path.exists('xp_data.json'):
            with open('xp_data.json', 'r') as f:
                xp_data = json.load(f)
                guild_id = str(interaction.guild.id)
                if guild_id in xp_data and str(member.id) in xp_data[guild_id]:
                    level = xp_data[guild_id][str(member.id)].get('level', 0)
                    xp = xp_data[guild_id][str(member.id)].get('xp', 0)
                    
        embed = discord.Embed(title=f"NETWORK DOSSIER: {member.name.upper()}", color=0xff1e1e)
        embed.add_field(name="Clearance Level", value=f"**Level {level}**\n({xp} XP)", inline=True)
        embed.add_field(name="Global Assets", value=f"**Wallet:** {wallet} ⌬\n**Vault:** {bank} ⌬", inline=True)
        
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        else:
            embed.set_thumbnail(url=member.default_avatar.url)
            
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
