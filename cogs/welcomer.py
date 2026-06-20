import discord
from discord.ext import commands
from discord import app_commands

class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="welcome")
        if not channel:
            channel = discord.utils.get(member.guild.text_channels, name="general")
            
        if channel:
            embed = discord.Embed(
                title=f"Welcome to {member.guild.name}!",
                description=f"Hey {member.mention}, we are so glad you are here!\n\n"
                            f"Make sure to read the rules and enjoy your stay. Feel free to ask if you need any help!",
                color=discord.Color.from_rgb(114, 137, 218)
            )
            
            if member.avatar:
                embed.set_thumbnail(url=member.avatar.url)
            else:
                embed.set_thumbnail(url=member.default_avatar.url)
                
            embed.set_footer(text=f"You are our {member.guild.member_count}th member! 🎉")
            
            await channel.send(content=f"Hello {member.mention}!", embed=embed)

    @app_commands.command(name='testwelcome', description='Test the welcome message embed locally.')
    @app_commands.checks.has_permissions(administrator=True)
    async def testwelcome(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Welcome to {interaction.guild.name}!",
            description=f"Hey {interaction.user.mention}, we are so glad you are here!\n\n"
                        f"Make sure to read the rules and enjoy your stay. Feel free to ask if you need any help!",
            color=discord.Color.from_rgb(114, 137, 218)
        )
        
        if interaction.user.avatar:
            embed.set_thumbnail(url=interaction.user.avatar.url)
        else:
            embed.set_thumbnail(url=interaction.user.default_avatar.url)
            
        embed.set_footer(text=f"You are our {interaction.guild.member_count}th member! 🎉")
        
        await interaction.response.send_message(content=f"Hello {interaction.user.mention}!", embed=embed)

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("❌ You must be an administrator to test the welcomer.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Welcomer(bot))
