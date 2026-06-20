import discord
from discord.ext import commands
from discord import app_commands

class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        import json
        import os
        channel = None
        if os.path.exists('server_config.json'):
            with open('server_config.json', 'r') as f:
                data = json.load(f)
                guild_id_str = str(member.guild.id)
                if guild_id_str in data and 'welcome_channel' in data[guild_id_str]:
                    channel = member.guild.get_channel(data[guild_id_str]['welcome_channel'])

        if not channel:
            channel = discord.utils.get(member.guild.text_channels, name="welcome")
        if not channel:
            channel = discord.utils.get(member.guild.text_channels, name="general")
            
        if channel:
            embed = discord.Embed(
                title=f"NEW TARGET ACQUIRED",
                description=f"> INITIALIZING CONNECTION...\n> CONNECTION SECURE.\n\nWelcome to the network, {member.mention}. Ensure your protocols are updated and read the server documentation.",
                color=0xff1e1e
            )
            
            if member.avatar:
                embed.set_thumbnail(url=member.avatar.url)
            else:
                embed.set_thumbnail(url=member.default_avatar.url)
                
            embed.set_footer(text=f"NETWORK NODE: {member.guild.member_count} CONNECTED")
            
            await channel.send(content=member.mention, embed=embed)

    @app_commands.command(name='testwelcome', description='Test the welcome message embed locally.')
    @app_commands.checks.has_permissions(administrator=True)
    async def testwelcome(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"NEW TARGET ACQUIRED",
            description=f"> INITIALIZING CONNECTION...\n> CONNECTION SECURE.\n\nWelcome to the network, {interaction.user.mention}. Ensure your protocols are updated and read the server documentation.",
            color=0xff1e1e
        )
        
        if interaction.user.avatar:
            embed.set_thumbnail(url=interaction.user.avatar.url)
        else:
            embed.set_thumbnail(url=interaction.user.default_avatar.url)
            
        embed.set_footer(text=f"NETWORK NODE: {interaction.guild.member_count} CONNECTED")
        
        await interaction.response.send_message(content=interaction.user.mention, embed=embed)

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("❌ You must be an administrator to test the welcomer.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Welcomer(bot))
