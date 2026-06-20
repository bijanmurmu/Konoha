import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from keep_alive import keep_alive

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Setup bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

class KonohaBot(commands.Bot):
    def __init__(self):
        # We still keep a text prefix just in case, but rely heavily on slash commands now
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        # Make sure cogs directory exists
        if not os.path.exists('./cogs'):
            os.makedirs('./cogs')

        # Load all python files in the cogs directory
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'Loaded module: {filename}')
                except Exception as e:
                    print(f'Failed to load module {filename}: {e}')
        
        # Sync the slash commands with Discord globally
        print("Syncing Slash Commands with Discord...")
        try:
            synced = await self.tree.sync()
            print(f"Successfully synced {len(synced)} Slash Commands.")
        except Exception as e:
            print(f"Failed to sync slash commands: {e}")

# Initialize bot
bot = KonohaBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

async def main():
    if not TOKEN or TOKEN == 'your_token_here':
        print("ERROR: Please paste your bot token into the .env file!")
        return
    
    # Start the background web server to keep the bot alive 24/7 on Render
    keep_alive()
    
    async with bot:
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
