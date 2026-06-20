import discord
from discord.ext import commands
import json
import os

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.threshold = 3

    def get_starboard_channel(self, guild_id):
        if os.path.exists('server_config.json'):
            with open('server_config.json', 'r') as f:
                data = json.load(f)
                guild_id_str = str(guild_id)
                if guild_id_str in data and 'starboard_channel' in data[guild_id_str]:
                    return data[guild_id_str]['starboard_channel']
        return None

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name != '⭐' and payload.emoji.name != '⭐':
            return
            
        guild = self.bot.get_guild(payload.guild_id)
        if not guild: return
        
        starboard_id = self.get_starboard_channel(guild.id)
        if not starboard_id: return
        
        starboard_channel = guild.get_channel(starboard_id)
        if not starboard_channel: return
        
        channel = guild.get_channel(payload.channel_id)
        if channel.id == starboard_id: return # Don't starboard the starboard
        
        try:
            message = await channel.fetch_message(payload.message_id)
        except:
            return
            
        # Count stars
        stars = 0
        for reaction in message.reactions:
            if reaction.emoji == '⭐' or getattr(reaction.emoji, 'name', '') == '⭐':
                stars = reaction.count
                break
                
        if stars >= self.threshold:
            # Check if already starboarded by searching past messages in starboard
            # Very basic check: just see if the message ID is in the recent history
            async for msg in starboard_channel.history(limit=50):
                if msg.embeds and str(message.id) in msg.embeds[0].footer.text:
                    return # Already posted
                    
            embed = discord.Embed(
                description=message.content,
                color=0xffd700 # Gold for starboard
            )
            embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
            
            if message.attachments:
                embed.set_image(url=message.attachments[0].url)
                
            embed.set_footer(text=f"ID: {message.id}")
            
            view = discord.ui.View()
            view.add_item(discord.ui.Button(label="Jump to Message", url=message.jump_url))
            
            await starboard_channel.send(content=f"⭐ **{stars}** {channel.mention}", embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Starboard(bot))
