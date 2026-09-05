import os
import discord
from discord.ext import commands
from ui_components import OrderView

# ----------------- DISCORD BOT SETUP -----------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    # ---- Memory optimizations (no logic changes) ----
    max_messages=200,                                     # default is 1000; we don't need a big message cache
    member_cache_flags=discord.MemberCacheFlags.none(),   # we never look users up via the member cache
    chunk_guilds_at_startup=False,                        # skip fetching full member lists on boot
)

# Remove the default help command to use our custom one
bot.remove_command('help')

# Track active order panels per (user_id, channel_id) to auto-close old ones
active_order_messages = {}


def clear_active_order(user_id, channel_id):
    """Remove a tracked order panel entry so the dict doesn't grow forever."""
    active_order_messages.pop((user_id, channel_id), None)


# ----------------- BOT COMMANDS -----------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is online!")


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

    view = OrderView(cleanup_callback=lambda: clear_active_order(ctx.author.id, ctx.channel.id))
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