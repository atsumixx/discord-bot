import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os
# ==========================================
# --- 1. WEB SERVER SETUP (FOR RENDER) ---
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Agency Bot is online and running!"

def run():
    app.run(host='0.0.0.0', port=8080)

# Start the web server in a background thread
Thread(target=run).start()


# ==========================================
# --- 2. DISCORD BOT SETUP ---
# ==========================================

# This creates the dropdown menu
class ExplorationSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Mondstadt", description="$7", value="mondstadt_7"),
            discord.SelectOption(label="Liyue", description="$10", value="liyue_10"),
            discord.SelectOption(label="Inazuma", description="$25", value="inazuma_25"),
            discord.SelectOption(label="Sumero (with desert)", description="$90", value="sumero_90"),
        ]
        super().__init__(placeholder="Choose an exploration area...", options=options)

    # This runs when a client picks an option
    async def callback(self, interaction: discord.Interaction):
        service, price = self.values[0].split('_')
        await interaction.response.send_message(
            f"Selected {service.title()} for ${price}. Sending to pilot board...", 
            ephemeral=True
        )

# This packages the dropdown into a View that Discord can display
class CommissionView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ExplorationSelect())

# This sets up the bot itself
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Bot is online and logged in as {bot.user}")

# The command you type in Discord to spawn the menu
@bot.command()
async def order(ctx):
    await ctx.send("Configure your commission below:", view=CommissionView())

# Run the bot
# Read the hidden token from Render's environment
token = os.getenv("DISCORD_TOKEN")
bot.run(token)