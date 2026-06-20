import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import random

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp_file = 'xp_data.json'
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.xp_file):
            with open(self.xp_file, 'r') as f:
                return json.load(f)
        return {}

    def save_data(self):
        with open(self.xp_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get_level(self, xp):
        # Proper RPG Leveling Curve: Level = 0.1 * sqrt(XP)
        # At 20 XP per msg: Level 1 requires 100 XP (5 msgs), Level 2 requires 400 XP (20 msgs).
        return int(0.1 * (xp ** 0.5))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
            
        user_id = str(message.author.id)
        guild_id = str(message.guild.id)
        
        if guild_id not in self.data:
            self.data[guild_id] = {}
            
        if user_id not in self.data[guild_id]:
            self.data[guild_id][user_id] = {'xp': 0, 'level': 0}
            
        # Give 15-25 XP per message
        xp_gain = random.randint(15, 25)
        self.data[guild_id][user_id]['xp'] += xp_gain
        
        current_xp = self.data[guild_id][user_id]['xp']
        current_level = self.data[guild_id][user_id]['level']
        new_level = self.get_level(current_xp)
        
        if new_level > current_level:
            self.data[guild_id][user_id]['level'] = new_level
            await message.channel.send(f"🎉 Congrats {message.author.mention}, you just advanced to **Level {new_level}**!")
            
        self.save_data()

    @app_commands.command(name='rank', description='Check your current level and XP.')
    async def rank(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        user_id = str(member.id)
        guild_id = str(interaction.guild.id)
        
        if guild_id in self.data and user_id in self.data[guild_id]:
            stats = self.data[guild_id][user_id]
            embed = discord.Embed(title=f"Rank: {member.name}", color=discord.Color.blue())
            embed.add_field(name="Level", value=stats['level'], inline=True)
            embed.add_field(name="Total XP", value=stats['xp'], inline=True)
            
            if member.avatar:
                embed.set_thumbnail(url=member.avatar.url)
            else:
                embed.set_thumbnail(url=member.default_avatar.url)
                
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"❌ {member.name} has no XP yet! Send some messages to level up.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Leveling(bot))
