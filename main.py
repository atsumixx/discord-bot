import os
import discord
from discord.ext import commands
from ui_components import OrderView

# ----------------- DISCORD BOT SETUP -----------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True        # Required for on_member_join to fire (welcome DM).
                               # Must also be enabled as "Server Members Intent"
                               # in the Discord Developer Portal for this bot.
intents.presences = False     # Presence updates are pure overhead here

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    max_messages=100,          # Default is 1000 cached messages; we never read history
    chunk_guilds_at_startup=False,  # Skip building the full member cache on boot
)

# Remove the default help command to use our custom one
bot.remove_command('help')

# Track active order panels per (user_id, channel_id) to auto-close old ones
active_order_messages = {}

# ----------------- BOT COMMANDS -----------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is online!")


@bot.event
async def on_member_join(member: discord.Member):
    if member.bot:
        return  # Don't DM other bots

    embed = discord.Embed(
        title="🌟 Welcome to Atsumi Piloting Services!",
        description=(
            f"Hey {member.mention}, welcome to the server! I'm **Paimon**, "
            "here to help you get set up with a commission whenever you're ready."
        ),
        color=discord.Color.from_rgb(255, 182, 193)  # Soft pink theme
    )

    embed.add_field(
        name="🗺️ What We Offer",
        value=(
            "Atsumi Piloting Services provides professional Genshin Impact piloting "
            "for:\n"
            "• **Map Exploration** — Mondstadt, Liyue, Inazuma, Sumeru, Fontaine, "
            "Natlan, Nod Krai, and more\n"
            "• **Special Areas** — Dragonspine, Chasm, Enkanomiya, and other "
            "sub-regions\n"
            "• **World Quests** — Region-specific quests needed to fully complete "
            "your exploration\n"
            "• **Character Maintenance** — Character ascension, weapon upgrades, "
            "artifact building, and talent leveling"
        ),
        inline=False
    )

    embed.add_field(
        name="🛒 How To Order",
        value=(
            "Type `!order` in any commission channel to open your interactive "
            "cart. From there you can:\n"
            "• Pick regions and special areas from the dropdown menus\n"
            "• Add required World Quests as they appear\n"
            "• Use the **+ Upgrade** button to add Character, Weapon, Artifact, "
            "or Talent building via quick forms\n"
            "• Hit **Submit** to confirm — this opens a private thread just for "
            "you and posts the job for our pilots\n\n"
            "Use `!help` any time for the full guide."
        ),
        inline=False
    )

    embed.add_field(
        name="📜 Server Rules & Regulations",
        value=(
            "To keep every transaction safe and professional, please follow "
            "these rules:\n"
            "1️⃣ All payments and account details are handled **only** in your "
            "private order thread with management or your assigned pilot.\n"
            "2️⃣ Never share your account password outside of the coordination "
            "steps management asks for — legitimate pilots will never ask you "
            "to change your account email or security settings.\n"
            "3️⃣ Payment is arranged **after** your order thread is created — "
            "do not send payment to anyone before that.\n"
            "4️⃣ Be respectful to staff, pilots, and other clients at all times.\n"
            "5️⃣ Do not advertise outside services or attempt to arrange deals "
            "off-platform.\n"
            "6️⃣ Report any suspicious behavior to a staff member immediately.\n"
            "7️⃣ Orders must be submitted through the `!order` menu — this keeps "
            "pricing accurate and every job tracked."
        ),
        inline=False
    )

    embed.set_footer(text="Atsumi Piloting Services • Type !order to begin your commission!")
    if member.guild.icon:
        embed.set_thumbnail(url=member.guild.icon.url)

    try:
        await member.send(embed=embed)
    except discord.Forbidden:
        # User has DMs disabled for the server / blocked the bot — nothing more we can do.
        print(f"[on_member_join] Could not DM {member} (DMs closed).")
    except discord.HTTPException as e:
        print(f"[on_member_join] Failed to DM {member}: {e}")


@bot.command()
async def help(ctx):
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    embed = discord.Embed(
        title="🌟 Atsumi Piloting Bot Guide",
        description="Here is everything you need to know about navigating the automated commission system.",
        color=discord.Color.from_rgb(255, 182, 193)  # Soft pink theme
    )

    embed.add_field(
        name="🛒 1. Placing an Order",
        value="Type `!order` to open the cart.\n"
              "• **Dropdowns:** Select map exploration or resin/talent maintenance.\n"
              "• **35% Discount:** If your map is over halfway done, pick the `(50% above Exploration)` tag for 35% off!\n"
              "• **Modals:** Use the blue buttons to type in Character/Weapon upgrades.",
        inline=False
    )
    
    embed.add_field(
        name="🗑️ 2. Fixing Mistakes",
        value="Added the wrong character levels? Click **Clear Custom Upgrades** in the `!order` menu to wipe your custom additions and try again.",
        inline=False
    )

    embed.add_field(
        name="💬 3. Managing Your Ticket",
        value="After submitting, a **Private Thread** is created. Inside, you can click **Edit / Replace Order** if you forgot something. The bot will remember your previous choices so you don't have to start from scratch.",
        inline=False
    )

    embed.add_field(
        name="⭐ 4. Completing the Deal",
        value="Once the pilot finishes the job, click **Mark Resolved & Review** in your thread. You'll be prompted to write a quick review, which automatically posts to `done-deal✔️` with your profile picture, and the bot will close your thread.",
        inline=False
    )

    embed.add_field(
        name="✈️ For Pilots",
        value="Keep an eye on `#available-job`. Click **Claim Job** to assign yourself, and **Mark Resolved** when you are completely finished with the account.",
        inline=False
    )

    embed.set_footer(text="Atsumi Piloting Services • Type !order to begin!")
    
    await ctx.send(embed=embed)


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

    view = OrderView(on_close=lambda: active_order_messages.pop(user_key, None))
    new_msg = await ctx.send(
        f"**Welcome to Atsumi Piloting Services, {ctx.author.mention}!**\n"
        "Customize your commission bundle below by selecting options from the menus or clicking the upgrade buttons, then click confirm.",
        view=view,
    )

    view.message = new_msg
    active_order_messages[user_key] = new_msg


# ----------------- RUN EVERYTHING -----------------
if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("ERROR: DISCORD_TOKEN environment variable not found!")