import discord
from discord.ext import commands
from discord import app_commands

class TicketButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="OPEN TICKET", style=discord.ButtonStyle.danger, custom_id="create_ticket_btn")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        
        # Create channel name
        channel_name = f"ticket-{user.name.lower()}"
        
        # Check if already exists
        existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
        if existing_channel:
            await interaction.response.send_message(f"> ERROR: YOU ALREADY HAVE AN ACTIVE TICKET: {existing_channel.mention}", ephemeral=True)
            return
            
        # Permissions
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        # Create Channel
        ticket_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
        
        # Send Welcome message in ticket
        embed = discord.Embed(
            title="SUPPORT TICKET OPENED",
            description=f"> INITIALIZING SUPPORT PROTOCOL...\n> SECURE CONNECTION ESTABLISHED.\n\nState your inquiry clearly. System administrators will respond shortly.",
            color=0xff1e1e
        )
        await ticket_channel.send(content=f"{user.mention}", embed=embed)
        await interaction.response.send_message(f"> TICKET CREATED: {ticket_channel.mention}", ephemeral=True)

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketButton())

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ticket_setup', description='Spawn the support ticket creation panel.')
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_setup(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="SYSTEM SUPPORT CENTER",
            description="Require assistance or administrative override? Click the button below to initialize a secure, encrypted ticket channel.",
            color=0xff1e1e
        )
        await interaction.channel.send(embed=embed, view=TicketView())
        await interaction.response.send_message("> TICKET PANEL INITIALIZED.", ephemeral=True)

    @app_commands.command(name='ticket_close', description='Close an active support ticket channel.')
    @app_commands.checks.has_permissions(manage_channels=True)
    async def ticket_close(self, interaction: discord.Interaction):
        if "ticket-" in interaction.channel.name:
            await interaction.response.send_message("> TERMINATING SUPPORT CHANNEL IN 5 SECONDS...")
            import asyncio
            await asyncio.sleep(5)
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("> ERROR: THIS IS NOT A TICKET CHANNEL.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Tickets(bot))
