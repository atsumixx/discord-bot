import discord
from config import EXPLORATION_PRICES, MAINTENANCE_PRICES


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
        f"Updated maintenance choices: {', '.join(self.values) if self.values else 'None'}",
        ephemeral=True,
    )


class OrderView(discord.ui.View):

  def __init__(self):
    super().__init__(timeout=180)
    self.selected_exploration = []
    self.selected_maintenance = []

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
          "⚠️ Please select at least one service from the dropdowns before"
          " submitting!",
          ephemeral=True,
      )
      return

    total_price = 0.0
    for item in self.selected_exploration:
      total_price += EXPLORATION_PRICES.get(item, 0.0)

    for item in self.selected_maintenance:
      total_price += MAINTENANCE_PRICES.get(item, 0.0)

    summary = f"📋 **New Commission Order from {interaction.user.mention}**\n"
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
        if self.selected_maintenance:
          job_board_msg += f"⚔️ **Maintenance:** {', '.join(self.selected_maintenance)}\n"
        job_board_msg += (
            f"💰 **Total Payout / Price:** `${total_price:.2f}`\n"
            f"📂 **Thread:** {ticket_thread.mention}"
        )
        await job_channel.send(job_board_msg)

      await interaction.followup.send(
          f"✅ Your order has been submitted! Head over to your private thread"
          f" {ticket_thread.mention} to finalize your payment of **${total_price:.2f}** with management.",
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
      row=2,
  )
  async def cancel_order(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.message.delete()