import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='purge', description='Deletes a specified number of messages.')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f'🧹 Successfully cleared {len(deleted)} messages.')

    @app_commands.command(name='kick', description='Kicks a member from the server.')
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(f'👢 **{member.name}** has been kicked. Reason: *{reason}*')
        except discord.Forbidden:
            await interaction.response.send_message("❌ I do not have permission to kick that member. Make sure my role is higher!", ephemeral=True)

    @app_commands.command(name='ban', description='Permanently bans a member from the server.')
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f'🔨 **{member.name}** has been permanently banned. Reason: *{reason}*')
        except discord.Forbidden:
            await interaction.response.send_message("❌ I do not have permission to ban that member. Make sure my role is higher!", ephemeral=True)

    @app_commands.command(name='tempban', description='Temporarily bans a member. Format: 10m, 2h, 1d')
    @app_commands.checks.has_permissions(ban_members=True)
    async def tempban(self, interaction: discord.Interaction, member: discord.Member, duration: str, reason: str = "No reason provided."):
        try:
            time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400}
            unit = duration[-1].lower()
            
            if unit not in time_dict:
                await interaction.response.send_message("❌ Invalid format! Use `s` (seconds), `m` (minutes), `h` (hours), or `d` (days). Example: `2h`", ephemeral=True)
                return
                
            time_val = int(duration[:-1])
            seconds = time_val * time_dict[unit]
            
            await member.ban(reason=f"Tempban: {reason}")
            await interaction.response.send_message(f'⏳ **{member.name}** has been temporarily banned for **{duration}**. Reason: *{reason}*')
            
            await asyncio.sleep(seconds)
            
            banned_users = [entry async for entry in interaction.guild.bans()]
            for ban_entry in banned_users:
                if ban_entry.user.id == member.id:
                    await interaction.guild.unban(ban_entry.user, reason="Temp-ban duration expired.")
                    break
                    
        except discord.Forbidden:
            await interaction.response.send_message("❌ I do not have permission to ban that member. Make sure my role is higher!", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Invalid number format! Example: `10m`", ephemeral=True)

    @app_commands.command(name='unban', description='Unbans a member by their exact Username or ID.')
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_identifier: str):
        banned_users = [entry async for entry in interaction.guild.bans()]
        
        for ban_entry in banned_users:
            user = ban_entry.user
            if user_identifier == str(user.id) or user_identifier.lower() == user.name.lower():
                await interaction.guild.unban(user, reason=f"Unbanned by {interaction.user.name}")
                await interaction.response.send_message(f'✅ **{user.name}** has been successfully unbanned and can rejoin the server!')
                return
                
        await interaction.response.send_message(f'❌ Could not find a banned user matching **{user_identifier}**.', ephemeral=True)

    @app_commands.command(name='bans', description='Shows a list of all currently banned users.')
    @app_commands.checks.has_permissions(ban_members=True)
    async def bans(self, interaction: discord.Interaction):
        banned_users = [entry async for entry in interaction.guild.bans()]
        
        if not banned_users:
            await interaction.response.send_message("✅ There are currently no banned users on this server!", ephemeral=True)
            return
            
        embed = discord.Embed(title=f"🔨 Banned Users in {interaction.guild.name}", color=discord.Color.red())
        
        ban_list = ""
        for idx, ban_entry in enumerate(banned_users, 1):
            user = ban_entry.user
            reason = ban_entry.reason if ban_entry.reason else "No reason provided"
            ban_list += f"**{idx}. {user.name}** (ID: `{user.id}`)\n*Reason: {reason}*\n\n"
            
        embed.description = ban_list
        await interaction.response.send_message(embed=embed)

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            if interaction.response.is_done():
                await interaction.followup.send("❌ You do not have permission to use this command.", ephemeral=True)
            else:
                await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
        else:
            if interaction.response.is_done():
                await interaction.followup.send(f"❌ An error occurred: {error}", ephemeral=True)
            else:
                await interaction.response.send_message(f"❌ An error occurred: {error}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
