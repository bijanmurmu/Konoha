import discord
from discord.ext import commands
import re

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Basic list of flagged words. Can be expanded dynamically later.
        self.banned_words = ['discord.gg/', 'free nitro', 'crypto scam'] 
        self.link_regex = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
            
        # Bypass for administrators
        if message.author.guild_permissions.administrator:
            return

        # Anti-Link System
        if self.link_regex.search(message.content):
            await message.delete()
            embed = discord.Embed(title="SECURITY ALERT", description=f"{message.author.mention} attempted to inject an unauthorized network link.\n\n**Action Taken:** Data Purged.", color=0xff1e1e)
            await message.channel.send(embed=embed, delete_after=8)
            return

        # Anti-Badword / Anti-Scam System
        content_lower = message.content.lower()
        if any(word in content_lower for word in self.banned_words):
            await message.delete()
            embed = discord.Embed(title="SECURITY ALERT", description=f"{message.author.mention} utilized a restricted protocol phrase.\n\n**Action Taken:** Data Purged.", color=0xff1e1e)
            await message.channel.send(embed=embed, delete_after=8)
            return

async def setup(bot):
    await bot.add_cog(Automod(bot))
