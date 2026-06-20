import discord
from discord.ext import commands
from discord import app_commands

class RoleButton(discord.ui.Button):
    def __init__(self, role: discord.Role):
        super().__init__(label=role.name, style=discord.ButtonStyle.primary, custom_id=f"role_{role.id}")
        self.role = role

    async def callback(self, interaction: discord.Interaction):
        # We must respond immediately or Discord shows "Interaction Failed"
        if self.role in interaction.user.roles:
            await interaction.user.remove_roles(self.role)
            await interaction.response.send_message(f"> ACCESS REVOKED: **{self.role.name}**", ephemeral=True)
        else:
            await interaction.user.add_roles(self.role)
            await interaction.response.send_message(f"> ACCESS GRANTED: **{self.role.name}**", ephemeral=True)

class RoleView(discord.ui.View):
    def __init__(self, roles):
        super().__init__(timeout=None) # Timeout=None makes it persistent forever
        for role in roles:
            self.add_item(RoleButton(role))

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='setup_roles', description='Setup a modern UI button role panel.')
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_roles(self, interaction: discord.Interaction, role1: discord.Role, role2: discord.Role = None, role3: discord.Role = None):
        # Gather the roles that were actually provided
        roles = [r for r in [role1, role2, role3] if r is not None]
        
        embed = discord.Embed(
            title="SYSTEM ACCESS PROTOCOLS", 
            description="Initialize your network clearance by selecting your protocols below.",
            color=0xff1e1e
        )
        
        view = RoleView(roles)
        # Send ephemeral confirmation to the admin
        await interaction.response.send_message("Role panel created successfully!", ephemeral=True)
        # Send the actual interactive UI panel to the channel
        await interaction.channel.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Roles(bot))
