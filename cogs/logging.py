import discord
from discord.ext import commands

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild):
        # Look for a channel named 'konoha-logs'
        channel = discord.utils.get(guild.text_channels, name="konoha-logs")
        if not channel:
            # If it doesn't exist, try to create it automatically
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            try:
                channel = await guild.create_text_channel('konoha-logs', overwrites=overwrites)
            except discord.Forbidden:
                return None
        return channel

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not message.guild:
            return
            
        log_channel = await self.get_log_channel(message.guild)
        if not log_channel: return
        
        embed = discord.Embed(title="🗑️ Message Deleted", color=discord.Color.red())
        embed.add_field(name="Author", value=message.author.mention, inline=True)
        embed.add_field(name="Channel", value=message.channel.mention, inline=True)
        embed.add_field(name="Content", value=message.content or "*No text (Media/Embed)*", inline=False)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or not before.guild or before.content == after.content:
            return
            
        log_channel = await self.get_log_channel(before.guild)
        if not log_channel: return
        
        embed = discord.Embed(title="✏️ Message Edited", color=discord.Color.orange())
        embed.add_field(name="Author", value=before.author.mention, inline=True)
        embed.add_field(name="Channel", value=before.channel.mention, inline=True)
        embed.add_field(name="Before", value=before.content or "*None*", inline=False)
        embed.add_field(name="After", value=after.content or "*None*", inline=False)
        await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logging(bot))
