import discord
import earnings_store as store

# ----------------- LOGIN CREDENTIALS -----------------
# Change these whenever you want to rotate the admin login.
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def build_admin_embed():
    summary = store.get_summary()
    records = store.get_all()

    embed = discord.Embed(
        title="🛠️ Atsumi Piloting — Admin Panel",
        color=discord.Color.from_rgb(255, 182, 193),
    )
    embed.add_field(
        name="💰 Totals",
        value=(
            f"**Commissions logged:** {summary['count']}\n"
            f"**Total revenue:** `${summary['total_revenue']:.2f}`\n"
            f"**Atsumi (15%):** `${summary['atsumi_total']:.2f}`\n"
            f"**Xylo (5%):** `${summary['xylo_total']:.2f}`"
        ),
        inline=False,
    )

    if summary["pilot_totals"]:
        pilot_lines = "\n".join(
            f"• {pilot}: `${amount:.2f}`"
            for pilot, amount in sorted(summary["pilot_totals"].items(), key=lambda x: -x[1])
        )
    else:
        pilot_lines = "No pilot earnings yet."
    embed.add_field(name="✈️ Pilot Earnings (80%)", value=pilot_lines, inline=False)

    if records:
        recent = records[-10:][::-1]
        recent_lines = "\n".join(
            f"`{r['id']}` {r['client']} → {r['pilot']} — `${r['total']:.2f}` "
            f"(pilot `${r['pilot_cut']:.2f}` / you `${r['atsumi_cut']:.2f}` / xylo `${r['xylo_cut']:.2f}`)"
            for r in recent
        )
    else:
        recent_lines = "No commissions recorded yet."
    embed.add_field(name="🧾 Recent Entries (id — client → pilot)", value=recent_lines[:1024], inline=False)

    embed.set_footer(text="Use the buttons below to add, edit, or delete an entry.")
    return embed


# ----------------- LOGIN -----------------
class AdminLoginModal(discord.ui.Modal, title="Admin Login"):
    username = discord.ui.TextInput(label="Username", required=True, max_length=50)
    password = discord.ui.TextInput(label="Password", required=True, max_length=50)

    async def on_submit(self, interaction: discord.Interaction):
        if self.username.value != ADMIN_USERNAME or self.password.value != ADMIN_PASSWORD:
            await interaction.response.send_message("⚠️ Incorrect username or password.", ephemeral=True)
            return
        panel_view = AdminPanelView()
        await interaction.response.send_message(embed=build_admin_embed(), view=panel_view)
        panel_view.message = await interaction.original_response()


class AdminLoginView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="Login", style=discord.ButtonStyle.blurple, emoji="🔐")
    async def login(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AdminLoginModal())


# ----------------- ADD / EDIT / DELETE MODALS -----------------
class AddEntryModal(discord.ui.Modal, title="Add Commission Entry"):
    client = discord.ui.TextInput(label="Client (name or mention)", required=True, max_length=100)
    pilot = discord.ui.TextInput(label="Pilot (name or mention)", required=True, max_length=100)
    total = discord.ui.TextInput(label="Total Price ($)", placeholder="e.g. 25.00", required=True, max_length=10)

    def __init__(self, panel_view):
        super().__init__()
        self.panel_view = panel_view

    async def on_submit(self, interaction: discord.Interaction):
        try:
            price = float(self.total.value)
        except ValueError:
            await interaction.response.send_message("⚠️ Total must be a number.", ephemeral=True)
            return
        store.add_manual_entry(self.client.value, self.pilot.value, price)
        await interaction.response.edit_message(embed=build_admin_embed(), view=self.panel_view)


class EditEntryModal(discord.ui.Modal, title="Edit Commission Entry"):
    entry_id = discord.ui.TextInput(label="Entry ID", placeholder="e.g. a1b2c3d4", required=True, max_length=8)
    total = discord.ui.TextInput(label="New Total ($) — leave blank to keep", required=False, max_length=10)
    pilot = discord.ui.TextInput(label="New Pilot — leave blank to keep", required=False, max_length=100)
    client = discord.ui.TextInput(label="New Client — leave blank to keep", required=False, max_length=100)

    def __init__(self, panel_view):
        super().__init__()
        self.panel_view = panel_view

    async def on_submit(self, interaction: discord.Interaction):
        price = None
        if self.total.value:
            try:
                price = float(self.total.value)
            except ValueError:
                await interaction.response.send_message("⚠️ Total must be a number.", ephemeral=True)
                return
        updated = store.edit_entry(
            self.entry_id.value.strip(),
            total=price,
            pilot=self.pilot.value.strip() or None,
            client=self.client.value.strip() or None,
        )
        if not updated:
            await interaction.response.send_message("⚠️ No entry found with that ID.", ephemeral=True)
            return
        await interaction.response.edit_message(embed=build_admin_embed(), view=self.panel_view)


class DeleteEntryModal(discord.ui.Modal, title="Delete Commission Entry"):
    entry_id = discord.ui.TextInput(label="Entry ID", placeholder="e.g. a1b2c3d4", required=True, max_length=8)

    def __init__(self, panel_view):
        super().__init__()
        self.panel_view = panel_view

    async def on_submit(self, interaction: discord.Interaction):
        deleted = store.delete_entry(self.entry_id.value.strip())
        if not deleted:
            await interaction.response.send_message("⚠️ No entry found with that ID.", ephemeral=True)
            return
        await interaction.response.edit_message(embed=build_admin_embed(), view=self.panel_view)


# ----------------- PANEL -----------------
class AdminPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)
        self.message = None

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        if self.message:
            try:
                await self.message.edit(view=self)
            except discord.HTTPException:
                pass

    @discord.ui.button(label="Refresh", style=discord.ButtonStyle.secondary, emoji="🔄")
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=build_admin_embed(), view=self)

    @discord.ui.button(label="Add Entry", style=discord.ButtonStyle.green, emoji="➕")
    async def add_entry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AddEntryModal(self))

    @discord.ui.button(label="Edit Entry", style=discord.ButtonStyle.blurple, emoji="✏️")
    async def edit_entry_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EditEntryModal(self))

    @discord.ui.button(label="Delete Entry", style=discord.ButtonStyle.danger, emoji="🗑️")
    async def delete_entry_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DeleteEntryModal(self))
