import discord
from config import EXPLORATION_PRICES, MAINTENANCE_PRICES

# ----------------- DROPDOWN SELECT MENUS -----------------
class ExplorationSelect(discord.ui.Select):
    def __init__(self, default_values=None):
        default_values = default_values or []
        options = [
            discord.SelectOption(label="Mondstadt (100%)", description="$7.00", emoji="🍃", value="Mondstadt (100%)"),
            discord.SelectOption(label="Mondstadt (>50% Progress)", description="$4.55 (35% OFF)", emoji="🍃", value="Mondstadt (>50%)"),
            discord.SelectOption(label="Liyue (100%)", description="$10.00", emoji="🔶", value="Liyue (100%)"),
            discord.SelectOption(label="Liyue (>50% Progress)", description="$6.50 (35% OFF)", emoji="🔶", value="Liyue (>50%)"),
            discord.SelectOption(label="Inazuma (100%)", description="$25.00", emoji="⚡", value="Inazuma (100%)"),
            discord.SelectOption(label="Inazuma (>50% Progress)", description="$16.25 (35% OFF)", emoji="⚡", value="Inazuma (>50%)"),
            discord.SelectOption(label="Sumeru with Desert (100%)", description="$90.00", emoji="🌿", value="Sumeru (100%)"),
            discord.SelectOption(label="Sumeru with Desert (>50% Progress)", description="$58.50 (35% OFF)", emoji="🌿", value="Sumeru (>50%)"),
            discord.SelectOption(label="Fontaine (100%)", description="$40.00", emoji="💧", value="Fontaine (100%)"),
            discord.SelectOption(label="Fontaine (>50% Progress)", description="$26.00 (35% OFF)", emoji="💧", value="Fontaine (>50%)"),
            discord.SelectOption(label="Natlan (100%)", description="$45.00", emoji="🔥", value="Natlan (100%)"),
            discord.SelectOption(label="Natlan (>50% Progress)", description="$29.25 (35% OFF)", emoji="🔥", value="Natlan (>50%)"),
            discord.SelectOption(label="Snezhnaya Archon (100%)", description="$40.00", emoji="❄️", value="Snezhnaya (100%)"),
            discord.SelectOption(label="Snezhnaya (>50% Progress)", description="$26.00 (35% OFF)", emoji="❄️", value="Snezhnaya (>50%)"),
            discord.SelectOption(label="Dragonspine (100%)", description="$8.00", emoji="🏔️", value="Dragonspine (100%)"),
            discord.SelectOption(label="Dragonspine (>50% Progress)", description="$5.20 (35% OFF)", emoji="🏔️", value="Dragonspine (>50%)"),
            discord.SelectOption(label="Chasm with underground (100%)", description="$15.00", emoji="🕳️", value="Chasm (100%)"),
            discord.SelectOption(label="Chasm (>50% Progress)", description="$9.75 (35% OFF)", emoji="🕳️", value="Chasm (>50%)"),
            discord.SelectOption(label="Chenyu Vale (100%)", description="$15.00", emoji="🍵", value="Chenyu Vale (100%)"),
            discord.SelectOption(label="Chenyu Vale (>50% Progress)", description="$9.75 (35% OFF)", emoji="🍵", value="Chenyu Vale (>50%)"),
            discord.SelectOption(label="Enkanomiya (100%)", description="$15.00", emoji="💠", value="Enkanomiya (100%)"),
            discord.SelectOption(label="Enkanomiya (>50% Progress)", description="$9.75 (35% OFF)", emoji="💠", value="Enkanomiya (>50%)"),
            discord.SelectOption(label="Sea of Bygone Eras (100%)", description="$15.00", emoji="🐚", value="Sea of Bygone Eras (100%)"),
            discord.SelectOption(label="Sea of Bygone Eras (>50%)", description="$9.75 (35% OFF)", emoji="🐚", value="Sea of Bygone Eras (>50%)"),
            discord.SelectOption(label="Ancient Sacred Mountain", description="$15.00", emoji="⛰️", value="Ancient Sacred Mountain (100%)"),
        ]
        
        for opt in options:
            if opt.value in default_values:
                opt.default = True

        super().__init__(placeholder="Select Exploration Services...", min_values=0, max_values=len(options), options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        view: OrderView = self.view
        view.selected_exploration = self.values
        await interaction.followup.send(f"Updated exploration choices: {', '.join(self.values) if self.values else 'None'}", ephemeral=True)


class MaintenanceSelect(discord.ui.Select):
    def __init__(self, default_values=None):
        default_values = default_values or []
        options = [
            discord.SelectOption(label="Artifacts Building (Resin)", description="$1.50", emoji="🏺", value="Artifacts Building ($1.50)"),
            discord.SelectOption(label="Talent Building (1-6)", description="$0.50", emoji="📜", value="Talent Building 1-6 ($0.50)"),
            discord.SelectOption(label="Talent Building (7-10)", description="$2.00", emoji="✨", value="Talent Building 7-10 ($2.00)"),
        ]
        for opt in options:
            if opt.value in default_values:
                opt.default = True

        super().__init__(placeholder="Select Other Character Maintenance...", min_values=0, max_values=len(options), options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        view: OrderView = self.view
        view.selected_maintenance = self.values
        await interaction.followup.send(f"Updated maintenance choices: {', '.join(self.values) if self.values else 'None'}", ephemeral=True)


# ----------------- MODALS -----------------
class CharacterAscensionModal(discord.ui.Modal, title="Character Ascension"):
    char_name = discord.ui.TextInput(label="Character Name", placeholder="e.g., Arlecchino", required=True, max_length=50)
    current_lvl = discord.ui.TextInput(label="Current Level", placeholder="e.g., 40", required=True, max_length=2)
    target_lvl = discord.ui.TextInput(label="Target Level", placeholder="e.g., 80", required=True, max_length=2)

    def __init__(self, cart_view):
        super().__init__()
        self.cart_view = cart_view

    async def on_submit(self, interaction: discord.Interaction):
        try:
            curr = int(self.current_lvl.value)
            targ = int(self.target_lvl.value)
            if curr >= targ or curr < 1 or targ > 90:
                await interaction.response.send_message("⚠️ Invalid levels!", ephemeral=True)
                return
            thresholds = [20, 40, 50, 60, 70, 80]
            ascensions_needed = sum(1 for t in thresholds if curr <= t < targ)
            price = ascensions_needed * 1.50
            cart_item = f"Char: {self.char_name.value} (Lv.{curr} ➡️ Lv.{targ}) - ${price:.2f}"
            self.cart_view.custom_maintenance.append(cart_item)
            self.cart_view.total_custom_price += price
            await interaction.response.send_message(f"✅ Added: **{cart_item}**", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("⚠️ Enter valid numbers!", ephemeral=True)


class WeaponUpgradeModal(discord.ui.Modal, title="Weapon Upgrade"):
    weapon_name = discord.ui.TextInput(label="Weapon Name", placeholder="e.g., Staff of Homa", required=True, max_length=50)
    current_lvl = discord.ui.TextInput(label="Current Level", placeholder="e.g., 1", required=True, max_length=2)
    target_lvl = discord.ui.TextInput(label="Target Level", placeholder="e.g., 90", required=True, max_length=2)

    def __init__(self, cart_view):
        super().__init__()
        self.cart_view = cart_view

    async def on_submit(self, interaction: discord.Interaction):
        try:
            curr = int(self.current_lvl.value)
            targ = int(self.target_lvl.value)
            if curr >= targ or curr < 1 or targ > 90:
                await interaction.response.send_message("⚠️ Invalid levels!", ephemeral=True)
                return
            thresholds = [20, 40, 50, 60, 70, 80]
            ascensions_needed = sum(1 for t in thresholds if curr <= t < targ)
            price = ascensions_needed * 1.50
            cart_item = f"Weapon: {self.weapon_name.value} (Lv.{curr} ➡️ Lv.{targ}) - ${price:.2f}"
            self.cart_view.custom_maintenance.append(cart_item)
            self.cart_view.total_custom_price += price
            await interaction.response.send_message(f"✅ Added: **{cart_item}**", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("⚠️ Enter valid numbers!", ephemeral=True)


# Client Feedback Modal when closing/resolving the deal
class ClientFeedbackModal(discord.ui.Modal, title="Commission Feedback & Review"):
    feedback = discord.ui.TextInput(
        label="Service & Pilot Feedback",
        style=discord.TextStyle.paragraph,
        placeholder="How was the service? Any shoutout for the pilot?",
        required=True,
        max_length=300
    )

    def __init__(self, summary_text, job_message):
        super().__init__()
        self.summary_text = summary_text
        self.job_message = job_message

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        guild = interaction.guild
        done_channel = discord.utils.get(guild.text_channels, name="done-deal✔️")
        
        # Format the final success post for the done-deal channel
        completion_embed_msg = (
            "✅ **COMPLETED COMMISSION / DEAL DONE**\n"
            f"{self.summary_text}\n\n"
            f"💬 **Client Review:** *\"{self.feedback.value}\"*\n"
            f"👤 **Client:** {interaction.user.mention}"
        )

        if done_channel:
            # 1. Post to done-deal channel
            await done_channel.send(completion_embed_msg)
            
            # 2. Move thread to the done-deal channel (Discord API allows moving threads under text channels)
            if isinstance(interaction.channel, discord.Thread):
                try:
                    # Move thread context / parent channel if supported, or lock/archive it
                    await interaction.channel.edit(name=f"done-{interaction.channel.name}", archived=True, locked=True)
                except Exception:
                    pass

        # 3. Update job board message to show green resolved state
        if self.job_message:
            try:
                new_job_content = self.job_message.content.replace("🟡 **Status:** In Progress", "🟢 **Status:** Completed & Reviewed")
                await self.job_message.edit(content=new_job_content, view=None)
            except discord.NotFound:
                pass

        await interaction.followup.send("🎉 Thank you! This order has been marked as resolved, reviewed, and archived.", ephemeral=True)
        
        try:
            await interaction.message.delete()
        except discord.NotFound:
            pass


# ----------------- JOB BOARD & THREAD VIEWS -----------------
class JobBoardView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.pilot = None

    @discord.ui.button(label="Claim Job", style=discord.ButtonStyle.blurple, emoji="🙋", custom_id="claim_btn")
    async def claim_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.pilot = interaction.user
        button.disabled = True
        button.label = "Claimed"
        button.style = discord.ButtonStyle.secondary
        for child in self.children:
            if getattr(child, "custom_id", "") == "resolve_btn":
                child.disabled = False
        current_content = interaction.message.content
        new_msg = current_content.replace("🔴 **Status:** Open (No Pilot)", f"🟡 **Status:** In Progress (Claimed by {self.pilot.mention})")
        await interaction.response.edit_message(content=new_msg, view=self)

    @discord.ui.button(label="Mark Resolved", style=discord.ButtonStyle.success, emoji="✅", disabled=True, custom_id="resolve_btn")
    async def resolve_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.pilot and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("⚠️ Only the claiming pilot or admin can resolve!", ephemeral=True)
            return
        button.disabled = True
        button.label = "Resolved"
        current_content = interaction.message.content
        new_msg = current_content.replace(f"🟡 **Status:** In Progress (Claimed by {self.pilot.mention})", f"🟢 **Status:** Resolved (Completed by {self.pilot.mention})")
        await interaction.response.edit_message(content=new_msg, view=self)


class ThreadManagementView(discord.ui.View):
    def __init__(self, job_message, summary_text, prev_expl=None, prev_maint=None, prev_custom=None, prev_custom_price=0.0):
        super().__init__(timeout=None)
        self.job_message = job_message
        self.summary_text = summary_text
        self.summary_message = None
        self.prev_expl = prev_expl or []
        self.prev_maint = prev_maint or []
        self.prev_custom = prev_custom or []
        self.prev_custom_price = prev_custom_price

    @discord.ui.button(label="Edit / Replace Order", style=discord.ButtonStyle.secondary, emoji="✏️", row=0)
    async def edit_order(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = OrderView(
            is_edit=True, 
            job_message=self.job_message, 
            summary_message=self.summary_message,
            initial_expl=self.prev_expl,
            initial_maint=self.prev_maint,
            initial_custom=self.prev_custom,
            initial_custom_price=self.prev_custom_price
        )
        await interaction.response.send_message("**Editing Order:** Update your selections below.", view=view, ephemeral=True)
        view.message = await interaction.original_response()

    @discord.ui.button(label="Mark Resolved & Review", style=discord.ButtonStyle.success, emoji="⭐", row=0)
    async def finish_and_review(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Trigger feedback modal for the client
        modal = ClientFeedbackModal(summary_text=self.summary_text, job_message=self.job_message)
        await interaction.response.send_modal(modal)


# ----------------- MAIN CART / ORDER VIEW -----------------
class OrderView(discord.ui.View):
    def __init__(self, is_edit=False, job_message=None, summary_message=None, 
                 initial_expl=None, initial_maint=None, initial_custom=None, initial_custom_price=0.0):
        super().__init__(timeout=180) 
        self.is_edit = is_edit
        self.job_message = job_message
        self.summary_message = summary_message
        
        self.selected_exploration = initial_expl or []
        self.selected_maintenance = initial_maint or []
        self.custom_maintenance = initial_custom.copy() if initial_custom else []
        self.total_custom_price = initial_custom_price

        self.add_item(ExplorationSelect(default_values=self.selected_exploration))
        self.add_item(MaintenanceSelect(default_values=self.selected_maintenance))

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        if self.message:
            try:
                await self.message.edit(content="⏱️ **Order session timed out.** Please type `!order` again.", view=self)
            except discord.NotFound:
                pass

    @discord.ui.button(label="Add Char Ascension", style=discord.ButtonStyle.blurple, emoji="📈", row=2)
    async def add_ascension(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CharacterAscensionModal(self))

    @discord.ui.button(label="Add Weapon Upgrade", style=discord.ButtonStyle.blurple, emoji="⚔️", row=2)
    async def add_weapon(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(WeaponUpgradeModal(self))

    @discord.ui.button(label="Clear Custom Upgrades", style=discord.ButtonStyle.danger, emoji="🗑️", row=2)
    async def clear_custom(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.custom_maintenance = []
        self.total_custom_price = 0.0
        await interaction.response.send_message("✅ Upgrades cleared.", ephemeral=True)

    @discord.ui.button(label="Confirm & Submit Order", style=discord.ButtonStyle.green, emoji="✅", row=3)
    async def submit_order(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        if not self.selected_exploration and not self.selected_maintenance and not self.custom_maintenance:
            await interaction.followup.send("⚠️ Please select at least one service!", ephemeral=True)
            return

        total_price = self.total_custom_price
        for item in self.selected_exploration:
            total_price += EXPLORATION_PRICES.get(item, 0.0)
        for item in self.selected_maintenance:
            total_price += MAINTENANCE_PRICES.get(item, 0.0)

        summary = f"📋 **{'Updated' if self.is_edit else 'New'} Commission Order from {interaction.user.mention}**\n"
        if self.selected_exploration:
            summary += f"\n🗺️ **Exploration:**\n- " + "\n- ".join(self.selected_exploration) + "\n"
        if self.custom_maintenance:
            summary += f"\n🛠️ **Custom Upgrades:**\n- " + "\n- ".join(self.custom_maintenance) + "\n"
        if self.selected_maintenance:
            summary += f"\n⚔️ **Other Maintenance:**\n- " + "\n- ".join(self.selected_maintenance) + "\n"
        summary += f"\n💰 **Estimated Total:** `${total_price:.2f}`"
        summary += "\n💳 *Please coordinate payment with management here before piloting begins.*"

        try:
            if self.is_edit:
                new_thread_view = ThreadManagementView(
                    job_message=self.job_message,
                    summary_text=summary,
                    prev_expl=self.selected_exploration,
                    prev_maint=self.selected_maintenance,
                    prev_custom=self.custom_maintenance,
                    prev_custom_price=self.total_custom_price
                )
                new_thread_view.summary_message = self.summary_message
                
                if self.summary_message:
                    await self.summary_message.edit(content=summary, view=new_thread_view)

                if self.job_message:
                    old_content = self.job_message.content
                    status_line = "🔴 **Status:** Open (No Pilot)"
                    for line in old_content.split('\n'):
                        if "**Status:**" in line:
                            status_line = line
                            break
                    
                    job_board_msg = (
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                        f"🆕 **Job Updated!**\n"
                        f"{status_line}\n"
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
                        f"📂 **Thread:** {self.summary_message.channel.mention}\n\n"
                    )
                    await self.job_message.edit(content=job_board_msg)

                await interaction.followup.send("✅ Your order has been successfully updated!", ephemeral=True)
                if self.message:
                    try:
                        await self.message.delete()
                    except discord.NotFound:
                        pass
                return

            # CREATE NEW ORDER
            thread_name = f"order-{interaction.user.name}"
            ticket_thread = await interaction.channel.create_thread(
                name=thread_name, type=discord.ChannelType.private_thread, invitable=False
            )
            await ticket_thread.add_user(interaction.user)

            job_channel = discord.utils.get(interaction.guild.text_channels, name="available-job")
            job_message = None
            if job_channel:
                job_board_msg = (
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"🆕 **New Job Available!**\n"
                    f"🔴 **Status:** Open (No Pilot)\n"
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
                    f"📂 **Thread:** {ticket_thread.mention}\n\n"
                )
                board_view = JobBoardView()
                job_message = await job_channel.send(job_board_msg, view=board_view)

            thread_view = ThreadManagementView(
                job_message=job_message,
                summary_text=summary,
                prev_expl=self.selected_exploration,
                prev_maint=self.selected_maintenance,
                prev_custom=self.custom_maintenance,
                prev_custom_price=self.total_custom_price
            )
            summary_msg = await ticket_thread.send(summary, view=thread_view)
            thread_view.summary_message = summary_msg

            await interaction.followup.send(
                f"✅ Your order has been submitted! Head over to your private thread {ticket_thread.mention} to finalize your payment of **${total_price:.2f}** with management.",
                ephemeral=True,
            )
        except Exception as e:
            await interaction.followup.send(f"⚠️ Failed to process order. Error: {e}", ephemeral=True)

    @discord.ui.button(label="Close / Cancel", style=discord.ButtonStyle.red, emoji="✖️", row=3)
    async def cancel_order(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        try:
            await interaction.message.delete()
        except discord.NotFound:
            pass