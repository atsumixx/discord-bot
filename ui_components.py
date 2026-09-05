import discord
import re

# ----------------- DYNAMIC WORLD QUEST DATA -----------------
# Maps base regions to their specific World Quests
WQ_DATA = {
    "Mondstadt": [
        {"label": "A long day in the mountain", "desc": "4-6 hrs", "val": "A long day in the mountain ($6)", "price": 6.0}
    ],
    "Liyue": [],
    "Inazuma": [
        {"label": "Sacred Sakura Cleansing", "desc": "2-4 hrs", "val": "Sacred Sakura Cleansing ($3.50)", "price": 3.5},
        {"label": "Tatara Tales", "desc": "2 hrs", "val": "Tatara Tales ($3)", "price": 3.0},
        {"label": "Orobashi Legacy", "desc": "2 hrs", "val": "Orobashi Legacy ($3)", "price": 3.0},
        {"label": "Moon Bathed Deep", "desc": "45 mins", "val": "Moon Bathed Deep ($1)", "price": 1.0},
        {"label": "Serai Stormchasers", "desc": "50 mins", "val": "Serai Stormchasers ($1)", "price": 1.0},
        {"label": "Through the Mist", "desc": "4 days", "val": "Through the Mist ($5.50)", "price": 5.5},
    ],
    "Sumeru": [
        {"label": "Aranyaka", "desc": "10-16 hrs", "val": "Aranyaka ($13)", "price": 13.0},
        {"label": "76 Aranara (Optional)", "desc": "Bonus", "val": "76 Aranara ($5.50)", "price": 5.5},
        {"label": "Golden Slumber", "desc": "Desert: 3-6 hrs", "val": "Golden Slumber ($7)", "price": 7.0},
        {"label": "Dual Evidence", "desc": "Desert: 2 hrs", "val": "Dual Evidence ($3)", "price": 3.0},
        {"label": "The Dirge of Bilqis", "desc": "Desert: 4-6 hrs", "val": "The Dirge of Bilqis ($7.50)", "price": 7.5},
        {"label": "Khvarena of Good and Evil", "desc": "Desert: 3-5 hrs", "val": "Khvarena of Good and Evil ($5)", "price": 5.0},
        {"label": "Soheil's wish", "desc": "Desert: 30 mins", "val": "Soheil's wish ($1)", "price": 1.0},
        {"label": "The falcon", "desc": "Desert: 1 hr", "val": "The falcon ($1.50)", "price": 1.5},
        {"label": "Her foes Rage like Great Waters", "desc": "Desert: 50 mins", "val": "Her foes Rage like Great Waters ($1.50)", "price": 1.5},
    ],
    "Fontaine": [
        {"label": "Narzissenkreuz Ordo Series", "desc": "5-7 hrs", "val": "Narzissenkreuz Ordo ($8.50)", "price": 8.5},
        {"label": "Fontaine Research Inst.", "desc": "2 hrs", "val": "Fontaine Research Inst ($3)", "price": 3.0},
        {"label": "Book of Esoteric Revelations", "desc": "1 hr", "val": "Book of Esoteric Revelations ($1.50)", "price": 1.5},
        {"label": "Wild Fairy of Erinyes", "desc": "1-2 hrs", "val": "Wild Fairy of Erinyes ($2.50)", "price": 2.5},
        {"label": "Canticles of Harmony", "desc": "2 hrs", "val": "Canticles of Harmony ($3)", "price": 3.0},
    ],
    "Natlan": [
        {"label": "Between Pledge and Forgettance", "desc": "2 hrs", "val": "Between Pledge and Forgettance ($3)", "price": 3.0},
        {"label": "Shadows of the Mountains", "desc": "1 hr", "val": "Shadows of the Mountains ($1.50)", "price": 1.5},
        {"label": "Tales of Dreams Plucked From Fire", "desc": "1-2 hrs", "val": "Tales of Dreams Plucked From Fire ($2.50)", "price": 2.5},
        {"label": "Bennett Story Part 1 & 2", "desc": "2 hrs", "val": "Bennett Story ($3)", "price": 3.0},
        {"label": "Atocpan Quest", "desc": "2-4 hrs", "val": "Atocpan Quest ($4)", "price": 4.0},
        {"label": "Ochkanantlan Quest", "desc": "2-3 hrs", "val": "Ochkanantlan Quest ($3.50)", "price": 3.5},
    ],
    "Nod Krai": [
        {"label": "Pahe Isle Quest", "desc": "45 mins", "val": "Pahe Isle Quest ($1)", "price": 1.0},
        {"label": "6 mini quests of Hiise Isle", "desc": "1 hr", "val": "Hiise Isle mini quests ($1.50)", "price": 1.5},
        {"label": "Illuga quest", "desc": "2 hrs", "val": "Illuga quest ($3)", "price": 3.0},
        {"label": "Moon Quest", "desc": "3 hrs", "val": "Moon Quest ($3.50)", "price": 3.5},
        {"label": "6 areas to submit sigils", "desc": "Not doing archon", "val": "Submit sigils ($1)", "price": 1.0},
    ]
}

# Automatically extracts the price from values like "Mondstadt ($10)"
def extract_price(item_str):
    match = re.search(r'\(\$([\d.]+)\)', item_str)
    return float(match.group(1)) if match else 0.0

# ----------------- DROPDOWN SELECT MENUS -----------------
class ExplorationSelect(discord.ui.Select):
    def __init__(self, default_values=None):
        default_values = default_values or []
        options = [
            discord.SelectOption(label="Mondstadt", description="$10.00", emoji="🍃", value="Mondstadt ($10)"),
            discord.SelectOption(label="Mondstadt (>50% Exploration)", description="$6.50", emoji="🍃", value="Mondstadt (>50%) ($6.50)"),
            discord.SelectOption(label="Liyue", description="$15.00", emoji="🔶", value="Liyue ($15)"),
            discord.SelectOption(label="Liyue (>50% Exploration)", description="$9.75", emoji="🔶", value="Liyue (>50%) ($9.75)"),
            discord.SelectOption(label="Inazuma", description="$25.00", emoji="⚡", value="Inazuma ($25)"),
            discord.SelectOption(label="Inazuma (>50% Exploration)", description="$16.25", emoji="⚡", value="Inazuma (>50%) ($16.25)"),
            discord.SelectOption(label="Sumeru (Forest & Desert)", description="$90.00", emoji="🌿", value="Sumeru ($90)"),
            discord.SelectOption(label="Sumeru (>50% Exploration)", description="$58.50", emoji="🌿", value="Sumeru (>50%) ($58.50)"),
            discord.SelectOption(label="Fontaine", description="$40.00", emoji="💧", value="Fontaine ($40)"),
            discord.SelectOption(label="Fontaine (>50% Exploration)", description="$26.00", emoji="💧", value="Fontaine (>50%) ($26.00)"),
            discord.SelectOption(label="Natlan", description="$45.00", emoji="🔥", value="Natlan ($45)"),
            discord.SelectOption(label="Natlan (>50% Exploration)", description="$29.25", emoji="🔥", value="Natlan (>50%) ($29.25)"),
            discord.SelectOption(label="Nod Krai", description="$45.00", emoji="🌌", value="Nod Krai ($45)"), # Update this price if needed
            discord.SelectOption(label="Nod Krai (>50% Exploration)", description="$29.25", emoji="🌌", value="Nod Krai (>50%) ($29.25)"),
        ]
        for opt in options:
            if opt.value in default_values:
                opt.default = True
        super().__init__(placeholder="Select Normal Exploration...", min_values=0, max_values=min(len(options), 25), options=options)

    async def callback(self, interaction: discord.Interaction):
        self.view.selected_exploration = self.values
        self.view.update_world_quest_dropdown()
        await interaction.response.edit_message(view=self.view)


class SpecialAreaSelect(discord.ui.Select):
    def __init__(self, default_values=None):
        default_values = default_values or []
        options = [
            discord.SelectOption(label="Dragonspine", description="$8.00", emoji="🏔️", value="Dragonspine ($8)"),
            discord.SelectOption(label="Windrest Peak", description="$10.00", emoji="⛰️", value="Windrest Peak ($10)"),
            discord.SelectOption(label="Temple of Space", description="$10.00", emoji="🏛️", value="Temple of Space ($10)"),
            discord.SelectOption(label="Chasm (with underground)", description="$13.00", emoji="🕳️", value="Chasm ($13)"),
            discord.SelectOption(label="Chenyu Vale", description="$13.00", emoji="🍵", value="Chenyu Vale ($13)"),
            discord.SelectOption(label="Enkanomiya", description="$15.00", emoji="💠", value="Enkanomiya ($15)"),
            discord.SelectOption(label="Sea of Bygone Eras", description="$13.00", emoji="🐚", value="Sea of Bygone Eras ($13)"),
            discord.SelectOption(label="Ancient Sacred Mountain", description="$13.00", emoji="🌋", value="Ancient Sacred Mountain ($13)"),
            discord.SelectOption(label="Frost Moon", description="$13.00", emoji="🌕", value="Frost Moon ($13)"),
        ]
        for opt in options:
            if opt.value in default_values:
                opt.default = True
        super().__init__(placeholder="Select Special Areas...", min_values=0, max_values=min(len(options), 25), options=options)

    async def callback(self, interaction: discord.Interaction):
        self.view.selected_special = self.values
        self.view.update_world_quest_dropdown()
        await interaction.response.edit_message(view=self.view)


class WorldQuestSelect(discord.ui.Select):
    def __init__(self, default_values=None):
        options = [discord.SelectOption(label="Select a region first...", value="none")]
        super().__init__(placeholder="Select Required World Quests...", min_values=0, max_values=1, options=options, disabled=True)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        self.view.selected_world_quests = self.values
        await interaction.followup.send(f"Updated World Quests: {', '.join(self.values) if self.values else 'None'}", ephemeral=True)


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
        self.view.selected_maintenance = self.values
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
        
        if done_channel:
            webhooks = await done_channel.webhooks()
            webhook = discord.utils.get(webhooks, name="PaimonLogger")
            if not webhook:
                webhook = await done_channel.create_webhook(name="PaimonLogger")
            client_user = interaction.user
            client_name = client_user.display_name
            client_avatar = client_user.display_avatar.url

            await webhook.send(content=self.feedback.value, username=client_name, avatar_url=client_avatar)
            clean_summary = self.summary_text.replace("\n💳 *Please coordinate payment with management here before piloting begins.*", "")

            embed = discord.Embed(
                title="✨ Commission Details & Summary",
                description=clean_summary,
                color=discord.Color.from_rgb(255, 182, 193)
            )
            embed.set_footer(text="Atsumi Piloting Services • Deal Completed Successfully")
            await done_channel.send(embed=embed)
            
            if isinstance(interaction.channel, discord.Thread):
                try:
                    await interaction.channel.edit(name=f"done-{interaction.channel.name}", archived=True, locked=True)
                except Exception:
                    pass

        if self.job_message:
            try:
                new_job_content = self.job_message.content.replace("🟡 **Status:** In Progress", "🟢 **Status:** Completed & Reviewed")
                await self.job_message.edit(content=new_job_content, view=None)
            except discord.NotFound:
                pass

        await interaction.followup.send("🎉 Thank you! Your review has been posted in `done-deal✔️` with your profile picture, and the order is archived.", ephemeral=True)
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
        new_msg = current_content.replace("🔴 **Status:** Open", "🟡 **Status:** In Progress")
        new_msg = new_msg.replace("✈️ **Pilot:** Unassigned", f"✈️ **Pilot:** {self.pilot.mention}")
        await interaction.response.edit_message(content=new_msg, view=self)

    @discord.ui.button(label="Mark Resolved", style=discord.ButtonStyle.success, emoji="✅", disabled=True, custom_id="resolve_btn")
    async def resolve_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.pilot and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("⚠️ Only the claiming pilot or admin can resolve!", ephemeral=True)
            return
        button.disabled = True
        button.label = "Resolved"
        current_content = interaction.message.content
        new_msg = current_content.replace("🟡 **Status:** In Progress", "🟢 **Status:** Resolved")
        await interaction.response.edit_message(content=new_msg, view=self)


class ThreadManagementView(discord.ui.View):
    def __init__(self, job_message, summary_text, prev_expl=None, prev_special=None, prev_wq=None, prev_maint=None, prev_custom=None, prev_custom_price=0.0):
        super().__init__(timeout=None)
        self.job_message = job_message
        self.summary_text = summary_text
        self.summary_message = None
        self.prev_expl = prev_expl or []
        self.prev_special = prev_special or []
        self.prev_wq = prev_wq or []
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
            initial_special=self.prev_special,
            initial_wq=self.prev_wq,
            initial_maint=self.prev_maint,
            initial_custom=self.prev_custom,
            initial_custom_price=self.prev_custom_price
        )
        await interaction.response.send_message("**Editing Order:** Update your selections below.", view=view, ephemeral=True)
        view.message = await interaction.original_response()

    @discord.ui.button(label="Mark Resolved & Review", style=discord.ButtonStyle.success, emoji="⭐", row=0)
    async def finish_and_review(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = ClientFeedbackModal(summary_text=self.summary_text, job_message=self.job_message)
        await interaction.response.send_modal(modal)


# ----------------- MAIN CART / ORDER VIEW -----------------
class OrderView(discord.ui.View):
    def __init__(self, is_edit=False, job_message=None, summary_message=None, 
                 initial_expl=None, initial_special=None, initial_wq=None, initial_maint=None, initial_custom=None, initial_custom_price=0.0):
        super().__init__(timeout=180) 
        self.is_edit = is_edit
        self.job_message = job_message
        self.summary_message = summary_message
        
        self.selected_exploration = initial_expl or []
        self.selected_special = initial_special or []
        self.selected_world_quests = initial_wq or []
        self.selected_maintenance = initial_maint or []
        self.custom_maintenance = initial_custom.copy() if initial_custom else []
        self.total_custom_price = initial_custom_price

        # Row 0
        self.add_item(ExplorationSelect(default_values=self.selected_exploration))
        # Row 1
        self.add_item(SpecialAreaSelect(default_values=self.selected_special))
        # Row 2
        self.wq_select = WorldQuestSelect()
        self.add_item(self.wq_select)
        # Row 3
        self.add_item(MaintenanceSelect(default_values=self.selected_maintenance))
        
        # Initialize WQ options dynamically based on initial values if editing
        self.update_world_quest_dropdown()

    def update_world_quest_dropdown(self):
        all_selected = self.selected_exploration + self.selected_special
        available_quests = []
        
        for region_val in all_selected:
            # Extracts base name (e.g., "Mondstadt (>50%) ($6.50)" -> "Mondstadt")
            clean_name = region_val.split(" (")[0].strip()
            
            if clean_name in ["Mondstadt", "Windrest Peak"]:
                quests = WQ_DATA.get("Mondstadt", [])
            elif clean_name == "Sumeru":
                quests = WQ_DATA.get("Sumeru", [])
            else:
                quests = WQ_DATA.get(clean_name, [])
                
            for q in quests:
                # Append if not already in list
                if not any(opt.value == q["val"] for opt in available_quests):
                    available_quests.append(discord.SelectOption(label=q["label"], description=q["desc"], value=q["val"]))

        if not available_quests:
            self.wq_select.options = [discord.SelectOption(label="Select a region first...", value="none")]
            self.wq_select.disabled = True
            self.wq_select.max_values = 1
            self.selected_world_quests = []
        else:
            self.wq_select.options = available_quests[:25] # Hard limit to prevent Discord crashes
            self.wq_select.disabled = False
            self.wq_select.max_values = len(self.wq_select.options)
            
            # Preserve valid active selections if menu changes
            valid_vals = [opt.value for opt in self.wq_select.options]
            self.selected_world_quests = [v for v in self.selected_world_quests if v in valid_vals]
            for opt in self.wq_select.options:
                if opt.value in self.selected_world_quests:
                    opt.default = True

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        if self.message:
            try:
                await self.message.edit(content="⏱️ **Order session timed out.** Please type `!order` again.", view=self)
            except discord.NotFound:
                pass

    @discord.ui.button(label="Ascension", style=discord.ButtonStyle.blurple, emoji="📈", row=4)
    async def add_ascension(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CharacterAscensionModal(self))

    @discord.ui.button(label="Weapon", style=discord.ButtonStyle.blurple, emoji="⚔️", row=4)
    async def add_weapon(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(WeaponUpgradeModal(self))

    @discord.ui.button(label="Clear", style=discord.ButtonStyle.danger, emoji="🗑️", row=4)
    async def clear_custom(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.custom_maintenance = []
        self.total_custom_price = 0.0
        await interaction.response.send_message("✅ Upgrades cleared.", ephemeral=True)

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.green, emoji="✅", row=4)
    async def submit_order(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        if not any([self.selected_exploration, self.selected_special, self.selected_world_quests, self.selected_maintenance, self.custom_maintenance]):
            await interaction.followup.send("⚠️ Please select at least one service!", ephemeral=True)
            return

        # Dynamically aggregate all selected dropdown values and extract their embedded prices
        total_price = self.total_custom_price
        all_items = self.selected_exploration + self.selected_special + self.selected_world_quests + self.selected_maintenance
        for item in all_items:
            total_price += extract_price(item)

        summary = f"📋 **{'Updated' if self.is_edit else 'New'} Commission Order from {interaction.user.mention}**\n"
        if self.selected_exploration:
            summary += f"\n🗺️ **Normal Exploration:**\n- " + "\n- ".join(self.selected_exploration) + "\n"
        if self.selected_special:
            summary += f"\n🧭 **Special Areas:**\n- " + "\n- ".join(self.selected_special) + "\n"
        if self.selected_world_quests:
            summary += f"\n📜 **World Quests:**\n- " + "\n- ".join(self.selected_world_quests) + "\n"
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
                    prev_special=self.selected_special,
                    prev_wq=self.selected_world_quests,
                    prev_maint=self.selected_maintenance,
                    prev_custom=self.custom_maintenance,
                    prev_custom_price=self.total_custom_price
                )
                new_thread_view.summary_message = self.summary_message
                
                if self.summary_message:
                    await self.summary_message.edit(content=summary, view=new_thread_view)

                if self.job_message:
                    old_content = self.job_message.content
                    status_line = "🔴 **Status:** Open"
                    pilot_line = "✈️ **Pilot:** Unassigned"
                    for line in old_content.split('\n'):
                        if "**Status:**" in line:
                            status_line = line
                        elif "**Pilot:**" in line:
                            pilot_line = line
                    
                    job_board_msg = (
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                        f"🆕 **Job Updated!**\n"
                        f"{status_line}\n"
                        f"👤 **Client:** {interaction.user.mention}\n"
                        f"{pilot_line}\n"
                    )
                    if self.selected_exploration:
                        job_board_msg += f"🗺️ **Normal Expl:** {', '.join(self.selected_exploration)}\n"
                    if self.selected_special:
                        job_board_msg += f"🧭 **Special Expl:** {', '.join(self.selected_special)}\n"
                    if self.selected_world_quests:
                        job_board_msg += f"📜 **Quests:** {', '.join(self.selected_world_quests)}\n"
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
                pilot_role = discord.utils.get(interaction.guild.roles, name="Pilot")
                role_ping = pilot_role.mention if pilot_role else "@Pilot"

                job_board_msg = (
                    f"{role_ping}\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"🆕 **New Job Available!**\n"
                    f"🔴 **Status:** Open\n"
                    f"👤 **Client:** {interaction.user.mention}\n"
                    f"✈️ **Pilot:** Unassigned\n"
                )
                if self.selected_exploration:
                    job_board_msg += f"🗺️ **Normal Expl:** {', '.join(self.selected_exploration)}\n"
                if self.selected_special:
                    job_board_msg += f"🧭 **Special Expl:** {', '.join(self.selected_special)}\n"
                if self.selected_world_quests:
                    job_board_msg += f"📜 **Quests:** {', '.join(self.selected_world_quests)}\n"
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
                prev_special=self.selected_special,
                prev_wq=self.selected_world_quests,
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

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="✖️", row=4)
    async def cancel_order(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        try:
            await interaction.message.delete()
        except discord.NotFound:
            pass