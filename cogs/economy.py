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
        embed = discord.Embed(title=f"GLOBAL RESERVE NODE: {member.name.upper()}", color=0xff1e1e)
        embed.add_field(name="Encrypted Wallet", value=f"**{stats['wallet']}** ⌬", inline=True)
        embed.add_field(name="Vault Storage", value=f"**{stats['bank']}** ⌬", inline=True)
        
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
            await interaction.response.send_message(f"> ERROR: ALLOWANCE TIMEOUT. NEXT PAYLOAD AVAILABLE IN **{hours}H {minutes}M**.", ephemeral=True)
            return
            
        reward = random.randint(100, 300)
        self.data[user_id]['wallet'] += reward
        self.data[user_id]['last_daily'] = now.isoformat()
        self.save_data()
        
        await interaction.response.send_message(f"> SYSTEM TRANSFER COMPLETE: **{reward} ⌬** DEPOSITED INTO ENCRYPTED WALLET.")

    @app_commands.command(name='leaderboard_wealth', description='Display the top 10 richest users in the global reserve.')
    async def leaderboard_wealth(self, interaction: discord.Interaction):
        # Sort users by wallet + bank
        sorted_users = sorted(
            self.data.items(), 
            key=lambda x: x[1].get('wallet', 0) + x[1].get('bank', 0), 
            reverse=True
        )[:10]
        
        embed = discord.Embed(title="GLOBAL RESERVE LEADERBOARD", color=0xff1e1e)
        
        desc = ""
        for i, (user_id, stats) in enumerate(sorted_users, 1):
            total = stats.get('wallet', 0) + stats.get('bank', 0)
            desc += f"**{i}.** <@{user_id}> - **{total}** ⌬\n"
            
        embed.description = desc or "> ERROR: NO RESERVE DATA FOUND."
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='pay', description='Transfer currency to another user.')
    async def pay(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        if amount <= 0:
            await interaction.response.send_message("> ERROR: INVALID TRANSFER AMOUNT.", ephemeral=True)
            return
            
        sender_id = str(interaction.user.id)
        receiver_id = str(member.id)
        
        self.init_user(sender_id)
        self.init_user(receiver_id)
        
        if self.data[sender_id]['wallet'] < amount:
            await interaction.response.send_message("> ERROR: INSUFFICIENT FUNDS FOR TRANSFER.", ephemeral=True)
            return
            
        self.data[sender_id]['wallet'] -= amount
        self.data[receiver_id]['wallet'] += amount
        self.save_data()
        
        await interaction.response.send_message(f"> TRANSFER SUCCESSFUL: **{amount} ⌬** ROUTED TO {member.mention}.")

async def setup(bot):
    await bot.add_cog(Economy(bot))
