import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import random
from datetime import datetime, timedelta

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.eco_file = 'economy_data.json'
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.eco_file):
            with open(self.eco_file, 'r') as f:
                return json.load(f)
        return {}

    def save_data(self):
        with open(self.eco_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def init_user(self, user_id):
        if user_id not in self.data:
            self.data[user_id] = {'wallet': 0, 'bank': 0, 'last_daily': "2000-01-01T00:00:00"}

    @app_commands.command(name='balance', description='Check your current global wallet and bank vault balances.')
    async def balance(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        user_id = str(member.id)
        
        self.init_user(user_id)
        
        stats = self.data[user_id]
        embed = discord.Embed(title=f"🏦 Central Bank: {member.name}", color=discord.Color.gold())
        embed.add_field(name="Wallet", value=f"**{stats['wallet']}** ⌬", inline=True)
        embed.add_field(name="Bank Vault", value=f"**{stats['bank']}** ⌬", inline=True)
        
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        else:
            embed.set_thumbnail(url=member.default_avatar.url)
            
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='daily', description='Claim your daily network allowance of global currency.')
    async def daily(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        self.init_user(user_id)
        
        last_claim = datetime.fromisoformat(self.data[user_id]['last_daily'])
        now = datetime.now()
        
        if now - last_claim < timedelta(days=1):
            time_left = timedelta(days=1) - (now - last_claim)
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            await interaction.response.send_message(f"⏳ You have already claimed your allowance! Please wait **{hours}h {minutes}m**.", ephemeral=True)
            return
            
        reward = random.randint(100, 300)
        self.data[user_id]['wallet'] += reward
        self.data[user_id]['last_daily'] = now.isoformat()
        self.save_data()
        
        await interaction.response.send_message(f"✅ You claimed your daily allowance of **{reward} ⌬**! It has been deposited into your wallet.")

async def setup(bot):
    await bot.add_cog(Economy(bot))
