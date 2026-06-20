import discord
from discord.ext import commands

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild):
        import json
        import os
        if os.path.exists('server_config.json'):
            with open('server_config.json', 'r') as f:
                data = json.load(f)
                guild_id_str = str(guild.id)
                if guild_id_str in data and 'log_channel' in data[guild_id_str]:
                    return guild.get_channel(data[guild_id_str]['log_channel'])

        # Fallback Look for a channel named 'konoha-logs'
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
        
        embed = discord.Embed(title="AUDIT LOG: DATA PURGED", color=0xff1e1e)
        embed.add_field(name="Target", value=message.author.mention, inline=True)
        embed.add_field(name="Sector", value=message.channel.mention, inline=True)
        embed.add_field(name="Payload", value=message.content or "*Encrypted/Media*", inline=False)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or not before.guild or before.content == after.content:
            return
            
        log_channel = await self.get_log_channel(before.guild)
        if not log_channel: return
        
        embed = discord.Embed(title="AUDIT LOG: DATA MODIFIED", color=0xff1e1e)
        embed.add_field(name="Target", value=before.author.mention, inline=True)
        embed.add_field(name="Sector", value=before.channel.mention, inline=True)
        embed.add_field(name="Initial Payload", value=before.content or "*None*", inline=False)
        embed.add_field(name="Modified Payload", value=after.content or "*None*", inline=False)
        await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logging(bot))
