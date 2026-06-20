import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = 'server_config.json'
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}

    def save_data(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get_guild_config(self, guild_id):
        guild_id_str = str(guild_id)
        if guild_id_str not in self.data:
            self.data[guild_id_str] = {}
        return self.data[guild_id_str]

    @app_commands.command(name='setup-welcome', description='Set the welcome channel for this server.')
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_welcome(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_config = self.get_guild_config(interaction.guild.id)
        guild_config['welcome_channel'] = channel.id
        self.save_data()
        await interaction.response.send_message(f"> SYSTEM UPDATE: Welcome protocols routed to {channel.mention}.", ephemeral=True)

    @app_commands.command(name='setup-logs', description='Set the audit log channel for this server.')
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_logs(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_config = self.get_guild_config(interaction.guild.id)
        guild_config['log_channel'] = channel.id
        self.save_data()
        await interaction.response.send_message(f"> SYSTEM UPDATE: Audit logs routed to {channel.mention}.", ephemeral=True)

    @app_commands.command(name='setup-starboard', description='Set the starboard channel for this server.')
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_starboard(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_config = self.get_guild_config(interaction.guild.id)
        guild_config['starboard_channel'] = channel.id
        self.save_data()
        await interaction.response.send_message(f"> SYSTEM UPDATE: Starboard tracking routed to {channel.mention}.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Config(bot))
