import os
import threading
from flask import Flask
import discord
from discord.ext import commands

# ----------------- FLASK SERVER (Keep-Alive for Render) -----------------
app = Flask("")


@app.route("/")
def home():
  return "Hello, World! Bot is running."


def run_flask():
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


def keep_alive():
  t = threading.Thread(target=run_flask)
  t.start()


# ----------------- DISCORD BOT SETUP -----------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# ----------------- DROPDOWN SELECT MENUS -----------------
class ExplorationSelect(discord.ui.Select):

  def __init__(self):
    options = [
        # Main Regions
        discord.SelectOption(
            label="Mondstadt", description="$7", emoji="🍃", value="Mondstadt"
        ),
        discord.SelectOption(
            label="Liyue", description="$10", emoji="🔶", value="Liyue"
        ),
        discord.SelectOption(
            label="Inazuma", description="$25", emoji="⚡", value="Inazuma"
        ),
        discord.SelectOption(
            label="Sumeru (with desert)",
            description="$90",
            emoji="🌿",
            value="Sumeru",
        ),
        discord.SelectOption(
            label="Fontaine", description="$40", emoji="💧", value="Fontaine"
        ),
        discord.SelectOption(
            label="Natlan", description="$45", emoji="🔥", value="Natlan"
        ),
        discord.SelectOption(
            label="Snezhnaya (Archon/World Quest)",
            description="$40",
            emoji="❄️",
            value="Snezhnaya",
        ),
        # Special Areas
        discord.SelectOption(
            label="Dragonspine",
            description="$8",
            emoji="🏔️",
            value="Dragonspine",
        ),
        discord.SelectOption(
            label="Windrise Peak",
            description="$5",
            emoji="🌬️",
            value="Windrise Peak",
        ),
        discord.SelectOption(
            label="Temple of Silence",
            description="$10",
            emoji="🏛️",
            value="Temple of Silence",
        ),
        discord.SelectOption(
            label="Chasm (with underground)",
            description="$15",
            emoji="🕳️",
            value="Chasm",
        ),
        discord.SelectOption(
            label="Chenyu Vale",
            description="$15",
            emoji="🍵",
            value="Chenyu Vale",
        ),
        discord.SelectOption(
            label="Enkanomiya",
            description="$15",
            emoji="💠",
            value="Enkanomiya",
        ),
        discord.SelectOption(
            label="Sea of Bygone Eras",
            description="$15",
            emoji="🐚",
            value="Sea of Bygone Eras",
        ),
        discord.SelectOption(
            label="Ancient Sacred Mountain",
            description="$15",
            emoji="⛰️",
            value="Ancient Sacred Mountain",
        ),
        discord.SelectOption(
            label="Frost Moon", description="$10", emoji="🌙", value="Frost Moon"
        ),
    ]
    super().__init__(
        placeholder="Select Exploration Services...",
        min_values=0,
        max_values=len(options),
        options=options,
    )

  async def callback(self, interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    view: OrderView = self.view
    view.selected_exploration = self.values
    await interaction.followup.send(
        f"Updated exploration choices: {', ' + ''.join(self.values) if self.values else 'None'}",
        ephemeral=True,
    )


class MaintenanceSelect(discord.ui.Select):

  def __init__(self):
    options = [
        discord.SelectOption(
            label="Character Ascend",
            description="$1.50 per ascension",
            emoji="📈",
            value="Character Ascend ($1.50)",
        ),
        discord.SelectOption(
            label="Weapon Upgrade",
            description="$1.50 per item",
            emoji="⚔️",
            value="Weapon Upgrade ($1.50)",
        ),
        discord.SelectOption(
            label="Artifacts Building (Resin Burn)",
            description="$1.50",
            emoji="🏺",
            value="Artifacts Building ($1.50)",
        ),
        discord.SelectOption(
            label="Talent Building (1-6)",
            description="$0.50",
            emoji="📜",
            value="Talent Building 1-6 ($0.50)",
        ),
        discord.SelectOption(
            label="Talent Building (7-10)",
            description="$2.00",
            emoji="✨",
            value="Talent Building 7-10 ($2.00)",
        ),
    ]
    super().__init__(
        placeholder="Select Character Maintenance...",
        min_values=0,
        max_values=len(options),
        options=options,
    )

  async def callback(self, interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    view: OrderView = self.view
    view.selected_maintenance = self.values
    await interaction.followup.send(
        f"Updated maintenance choices: {', ' + ''.join(self.values) if self.values else 'None'}",
        ephemeral=True,
    )


# ----------------- MAIN CART / ORDER VIEW -----------------
class OrderView(discord.ui.View):

  def __init__(self):
    super().__init__(timeout=180)
    self.selected_exploration = []
    self.selected_maintenance = []

    # Add the dropdowns to the view
    self.add_item(ExplorationSelect())
    self.add_item(MaintenanceSelect())

  @discord.ui.button(
      label="Confirm & Submit Order",
      style=discord.ButtonStyle.green,
      emoji="✅",
      row=2,
  )
  async def submit_order(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.response.defer(ephemeral=True)

    if not self.selected_exploration and not self.selected_maintenance:
      await interaction.followup.send(
          "⚠️ Please select at least one service from the dropdowns before submitting!",
          ephemeral=True,
      )
      return

    summary = "**📋 Atsumi Piloting Services - Order Summary**\n"
    if self.selected_exploration:
      summary += (
          f"\n🗺️ **Exploration:**\n- "
          + "\n- ".join(self.selected_exploration)
          + "\n"
      )
    if self.selected_maintenance:
      summary += (
          f"\n⚔️ **Character Maintenance:**\n- "
          + "\n- ".join(self.selected_maintenance)
          + "\n"
      )

    summary += (
        "\n🚀 *Your package has been successfully bundled and sent to the pilot"
        " board!*"
    )

    await interaction.followup.send(summary, ephemeral=True)


# ----------------- BOT COMMANDS -----------------
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


# ----------------- RUN EVERYTHING -----------------
if __name__ == "__main__":
  keep_alive()
  TOKEN = os.getenv("DISCORD_TOKEN")
  if TOKEN:
    bot.run(TOKEN)
  else:
    print("ERROR: DISCORD_TOKEN environment variable not found!")