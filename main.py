import os
import threading
from flask import Flask
import discord
from discord.ext import commands
from views.order_view import OrderView

# Flask Keep-Alive for Render
app = Flask("")


@app.route("/")
def home():
  return "Bot is running."


def run_flask():
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


def keep_alive():
  t = threading.Thread(target=run_flask)
  t.start()


# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
  print(f"Logged in as {bot.user} (ID: {bot.user.id})")
  print("Bot is online!")


@bot.command()
async def order(ctx):
  view = OrderView()
  await ctx.send(
      "**Welcome to Atsumi Piloting Services!**\nCustomize your commission"
      " bundle below by selecting options from the menus, then click confirm.",
      view=view,
  )


if __name__ == "__main__":
  keep_alive()
  TOKEN = os.getenv("DISCORD_TOKEN")
  if TOKEN:
    bot.run(TOKEN)
  else:
    print("ERROR: DISCORD_TOKEN environment variable not found!")