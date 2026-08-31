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

# Track active order panels per (user_id, channel_id) to auto-close old ones
active_order_messages = {}


# ----------------- DROPDOWN SELECT MENUS -----------------
class ExplorationSelect(discord.ui.Select):

  def __init__(self):
    options = [
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
        f"Updated exploration choices: {', '.join(self.values) if self.values else 'None'}",
        ephemeral=True,
    )


class MaintenanceSelect(discord.ui.Select):

  def __init__(self):
    options = [
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
        placeholder="Select Other Character Maintenance...",
        min_values=0,
        max_values=len(options),
        options=options,
    )

  async def callback(self, interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    view: OrderView = self.view
    view.selected_maintenance = self.values
    await interaction.followup.send(
        f"Updated maintenance choices: {', '.join(self.values) if self.values else 'None'}",
        ephemeral=True,
    )


# ----------------- MODALS (POP-UP FORMS) -----------------
class CharacterAscensionModal(discord.ui.Modal, title="Character Ascension"):

  char_name = discord.ui.TextInput(
      label="Character Name",
      placeholder="e.g., Arlecchino",
      required=True,
      max_length=50,
  )
  current_lvl = discord.ui.TextInput(
      label="Current Level",
      placeholder="e.g., 40",
      required=True,
      max_length=2,
  )
  target_lvl = discord.ui.TextInput(
      label="Target Level",
      placeholder="e.g., 80",
      required=True,
      max_length=2,
  )

  def __init__(self, cart_view):
    super().__init__()
    self.cart_view = cart_view

  async def on_submit(self, interaction: discord.Interaction):
    try:
      curr = int(self.current_lvl.value)
      targ = int(self.target_lvl.value)

      if curr >= targ or curr < 1 or targ > 90:
        await interaction.response.send_message(
            "⚠️ Invalid levels! Target level must be higher than current level,"
            " max level is 90.",
            ephemeral=True,
        )
        return

      thresholds = [20, 40, 50, 60, 70, 80]
      ascensions_needed = sum(1 for t in thresholds if curr <= t < targ)
      price = ascensions_needed * 1.50

      cart_item = (
          f"Char: {self.char_name.value} (Lv.{curr} ➡️ Lv.{targ}) - ${price:.2f}"
      )

      self.cart_view.custom_maintenance.append(cart_item)
      self.cart_view.total_custom_price += price

      await interaction.response.send_message(
          f"✅ Added to cart: **{cart_item}**", ephemeral=True
      )

    except ValueError:
      await interaction.response.send_message(
          "⚠️ Please enter valid numbers for the levels!", ephemeral=True
      )


class WeaponUpgradeModal(discord.ui.Modal, title="Weapon Upgrade"):

  weapon_name = discord.ui.TextInput(
      label="Weapon Name",
      placeholder="e.g., Staff of Homa",
      required=True,
      max_length=50,
  )
  current_lvl = discord.ui.TextInput(
      label="Current Level",
      placeholder="e.g., 1",
      required=True,
      max_length=2,
  )
  target_lvl = discord.ui.TextInput(
      label="Target Level",
      placeholder="e.g., 90",
      required=True,
      max_length=2,
  )

  def __init__(self, cart_view):
    super().__init__()
    self.cart_view = cart_view

  async def on_submit(self, interaction: discord.Interaction):
    try:
      curr = int(self.current_lvl.value)
      targ = int(self.target_lvl.value)

      if curr >= targ or curr < 1 or targ > 90:
        await interaction.response.send_message(
            "⚠️ Invalid levels! Target level must be higher than current level,"
            " max level is 90.",
            ephemeral=True,
        )
        return

      thresholds = [20, 40, 50, 60, 70, 80]
      ascensions_needed = sum(1 for t in thresholds if curr <= t < targ)
      price = ascensions_needed * 1.50

      cart_item = (
          f"Weapon: {self.weapon_name.value} (Lv.{curr} ➡️ Lv.{targ}) -"
          f" ${price:.2f}"
      )

      self.cart_view.custom_maintenance.append(cart_item)
      self.cart_view.total_custom_price += price

      await interaction.response.send_message(
          f"✅ Added weapon to cart: **{cart_item}**", ephemeral=True
      )

    except ValueError:
      await interaction.response.send_message(
          "⚠️ Please enter valid numbers for the levels!", ephemeral=True
      )


# ----------------- MAIN CART / ORDER VIEW -----------------
class OrderView(discord.ui.View):

  def __init__(self):
    super().__init__(timeout=180)  # Times out after 3 minutes
    self.message = None
    self.selected_exploration = []
    self.selected_maintenance = []

    self.custom_maintenance = []
    self.total_custom_price = 0.0

    self.add_item(ExplorationSelect())
    self.add_item(MaintenanceSelect())

  async def on_timeout(self):
    for child in self.children:
      child.disabled = True
    if self.message:
      try:
        await self.message.edit(
            content=(
                "⏱️ **Order session timed out.** Please type `!order` again to"
                " start a new order."
            ),
            view=self,
        )
      except discord.NotFound:
        pass

  @discord.ui.button(
      label="Add Character Ascension",
      style=discord.ButtonStyle.blurple,
      emoji="📈",
      row=2,
  )
  async def add_ascension(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.response.send_modal(CharacterAscensionModal(self))

  @discord.ui.button(
      label="Add Weapon Upgrade",
      style=discord.ButtonStyle.blurple,
      emoji="⚔️",
      row=2,
  )
  async def add_weapon(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.response.send_modal(WeaponUpgradeModal(self))

  @discord.ui.button(
      label="Confirm & Submit Order",
      style=discord.ButtonStyle.green,
      emoji="✅",
      row=3,
  )
  async def submit_order(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.response.defer(ephemeral=True)

    if (
        not self.selected_exploration
        and not self.selected_maintenance
        and not self.custom_maintenance
    ):
      await interaction.followup.send(
          "⚠️ Please select at least one service before submitting!",
          ephemeral=True,
      )
      return

    total_price = self.total_custom_price

    exploration_prices = {
        "Mondstadt": 7.0,
        "Liyue": 10.0,
        "Inazuma": 25.0,
        "Sumeru": 90.0,
        "Fontaine": 40.0,
        "Natlan": 45.0,
        "Snezhnaya": 40.0,
        "Dragonspine": 8.0,
        "Windrise Peak": 5.0,
        "Temple of Silence": 10.0,
        "Chasm": 15.0,
        "Chenyu Vale": 15.0,
        "Enkanomiya": 15.0,
        "Sea of Bygone Eras": 15.0,
        "Ancient Sacred Mountain": 15.0,
        "Frost Moon": 10.0,
    }

    maintenance_prices = {
        "Artifacts Building ($1.50)": 1.50,
        "Talent Building 1-6 ($0.50)": 0.50,
        "Talent Building 7-10 ($2.00)": 2.00,
    }

    for item in self.selected_exploration:
      total_price += exploration_prices.get(item, 0.0)

    for item in self.selected_maintenance:
      total_price += maintenance_prices.get(item, 0.0)

    summary = f"📋 **New Commission Order from {interaction.user.mention}**\n"
    if self.selected_exploration:
      summary += (
          f"\n🗺️ **Exploration:**\n- "
          + "\n- ".join(self.selected_exploration)
          + "\n"
      )
    if self.custom_maintenance:
      summary += (
          f"\n🛠️ **Custom Upgrades:**\n- "
          + "\n- ".join(self.custom_maintenance)
          + "\n"
      )
    if self.selected_maintenance:
      summary += (
          f"\n⚔️ **Other Maintenance:**\n- "
          + "\n- ".join(self.selected_maintenance)
          + "\n"
      )

    summary += f"\n💰 **Estimated Total:** `${total_price:.2f}`"
    summary += (
        "\n💳 *Please coordinate payment with management here before piloting"
        " begins.*"
    )

    try:
      thread_name = f"order-{interaction.user.name}"
      ticket_thread = await interaction.channel.create_thread(
          name=thread_name,
          type=discord.ChannelType.private_thread,
          invitable=False,
      )
      await ticket_thread.add_user(interaction.user)
      await ticket_thread.send(summary)

      job_channel = discord.utils.get(
          interaction.guild.text_channels, name="available-job"
      )
      if job_channel:
        job_board_msg = (
            f"🆕 **New Job Available!**\n"
            f"👤 **Client:** {interaction.user.mention}\n"
        )
        if self.selected_exploration:
          job_board_msg += f"🗺️ **Exploration:** {', '.join(self.selected_exploration)}\n"
        if self.custom_maintenance:
          job_board_msg += f"🛠️ **Upgrades:** {', '.join(self.custom_maintenance)}\n"
        if self.selected_maintenance:
          job_board_msg += f"⚔️ **Maintenance:** {', '.join(self.selected_maintenance)}\n"

        job_board_msg += (
            f"💰 **Total Price:** `${total_price:.2f}`\n"
            f"📂 **Thread:** {ticket_thread.mention}"
        )
        await job_channel.send(job_board_msg)

      await interaction.followup.send(
          f"✅ Your order has been submitted! Head over to your private thread"
          f" {ticket_thread.mention} to finalize your payment of"
          f" **${total_price:.2f}** with management.",
          ephemeral=True,
      )
    except Exception as e:
      await interaction.followup.send(
          f"⚠️ Failed to process order. Error: {e}", ephemeral=True
      )

  @discord.ui.button(
      label="Close / Cancel",
      style=discord.ButtonStyle.red,
      emoji="✖️",
      row=3,
  )
  async def cancel_order(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.message.delete()


# ----------------- BOT COMMANDS -----------------
@bot.event
async def on_ready():
  print(f"Logged in as {bot.user} (ID: {bot.user.id})")
  print("Bot is online!")


@bot.command()
async def order(ctx):
  # Deletes the user's "!order" command message
  try:
    await ctx.message.delete()
  except discord.Forbidden:
    pass

  # Deletes any existing active order message for this user in this channel
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
      "Customize your commission bundle below by selecting options from the"
      " menus or clicking the upgrade buttons, then click confirm.",
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