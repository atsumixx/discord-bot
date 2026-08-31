import os
import discord
from discord.ext import commands
from keep_alive import keep_alive
from ui_components import OrderView

# ----------------- DISCORD BOT SETUP -----------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Track active order panels per (user_id, channel_id) to auto-close old ones
active_order_messages = {}

# ----------------- BOT COMMANDS -----------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is online!")

@bot.command()
async def order(ctx):
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    user_key = (ctx.author.id, ctx.channel.id)
    if user_key in active_order_messages:
        old_msg = active_order_messages[user_key]
        try:
            await old_msg.delete()
        except discord.NotFound:
            pass

    view = OrderView()
    new_msg = await ctx.send(
        f"**Welcome to Atsumi Piloting Services, {ctx.author.mention}!**\n"
        "Customize your commission bundle below by selecting options from the menus or clicking the upgrade buttons, then click confirm.",
        view=view,
    )

    view.message = new_msg
    active_order_messages[user_key] = new_msg

# ----------------- RUN EVERYTHING -----------------
if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("ERROR: DISCORD_TOKEN environment variable not found!")