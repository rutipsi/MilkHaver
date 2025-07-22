<<<<<<< HEAD
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import datetime

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.bans = True
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

# Load IDs from environment variables
ROLE_ID = int(os.getenv("ROLE_ID"))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

def human_time_delta(td):
    seconds = int(td.total_seconds())
    times = []
    periods = [
        ('yr', 60*60*24*365),
        ('mo', 60*60*24*30),
        ('d', 60*60*24),
        ('hr', 60*60),
        ('min', 60),
        ('sec', 1)
    ]
    for suffix, length in periods:
        val, seconds = divmod(seconds, length)
        if val > 0:
            times.append(f"{val}{suffix}")
    return '-'.join(times)

@commands.check
async def global_role_check(ctx):
    if isinstance(ctx.author, discord.Member):
        return any(role.id == ROLE_ID for role in ctx.author.roles)
    return False

class MyCommandTree(discord.app_commands.CommandTree):
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if isinstance(interaction.user, discord.Member):
            if any(role.id == ROLE_ID for role in interaction.user.roles):
                return True
        await interaction.response.send_message(
            "You do not have permission to use this command.",
            ephemeral=True
        )
        return False

bot = commands.Bot(
    command_prefix="9",
    intents=intents,
    tree_cls=MyCommandTree
)

bot.add_check(global_role_check)

@bot.event
async def on_ready():
    await bot.tree.sync()  # Global slash command sync (may take up to 1h for new cmds)
    print(f'Bot is online! Logged in as {bot.user}')

@bot.event
async def on_member_remove(member):
    # Don't act on bots
    if member.bot:
        return
    now = discord.utils.utcnow()
    joined = member.joined_at or now
    time_in = now - joined
    time_str = human_time_delta(time_in)
    channel_counts = {}
    try:
        for channel in member.guild.text_channels:
            count = 0
            try:
                async for msg in channel.history(limit=800, oldest_first=False):
                    if msg.author == member:
                        count += 1
                if count > 0:
                    channel_counts[channel.name] = count
            except (discord.Forbidden, discord.HTTPException):
                continue
    except Exception:
        channel_counts = {}

    details = [
        "<:v1:1396702889002401792><:v2:1396702906387796059><:v3:1396702922007515286>_**BANNED**_<:v1:1396702889002401792><:v2:1396702906387796059><:v3:1396702922007515286>",
        f"## **{member}** ({member.id})",
        f"Joined: ",
        f"Left: ",
        f"Stayed: {time_str}"
    ]
    if channel_counts:
        ch_reports = [f"{ch} - {cnt}msg" for ch, cnt in channel_counts.items()]
        details.append("Messages: " + "; ".join(ch_reports))
    else:
        details.append("Messages: none")

    details.append(
        "<:v1:1396702889002401792><:v2:1396702906387796059><:v2:1396702906387796059><:v2:1396702906387796059><:v2:1396702906387796059><:v3:1396702922007515286>"
    )
    report = "\n".join(details)
    log_channel = member.guild.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(report)
    try:
        await member.ban(reason="Auto-ban: user left the server.")
    except Exception as e:
        if log_channel:
            await log_channel.send(f"Failed to ban {member}: {e}")

@bot.command()
async def bulkban(ctx, *user_ids):
    banned = []
    failed = []
    for uid in user_ids:
        try:
            await ctx.guild.ban(discord.Object(id=int(uid)), reason="Bulk ban")
            banned.append(uid)
        except Exception as e:
            failed.append(f"{uid} ({e})")
    result = f"Banned: {', '.join(banned)}"
    if failed:
        result += f"\nFailed: {', '.join(failed)}"
    await ctx.send(result)

@bot.tree.command(name="bulkban", description="Ban multiple users by their IDs")
async def slash_bulkban(interaction: discord.Interaction, user_ids: str):
    ids = user_ids.split()
    banned = []
    failed = []
    for uid in ids:
        try:
            await interaction.guild.ban(discord.Object(id=int(uid)), reason="Bulk ban (slash command)")
            banned.append(uid)
        except Exception as e:
            failed.append(f"{uid} ({e})")
    reply = f"Banned: {', '.join(banned)}"
    if failed:
        reply += f"\nFailed: {', '.join(failed)}"
    await interaction.response.send_message(reply, ephemeral=True)

bot.run(TOKEN)
=======
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import datetime

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.bans = True
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

# Load IDs from environment variables
ROLE_ID = int(os.getenv("ROLE_ID"))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

def human_time_delta(td):
    seconds = int(td.total_seconds())
    times = []
    periods = [
        ('yr', 60*60*24*365),
        ('mo', 60*60*24*30),
        ('d', 60*60*24),
        ('hr', 60*60),
        ('min', 60),
        ('sec', 1)
    ]
    for suffix, length in periods:
        val, seconds = divmod(seconds, length)
        if val > 0:
            times.append(f"{val}{suffix}")
    return '-'.join(times)

@commands.check
async def global_role_check(ctx):
    if isinstance(ctx.author, discord.Member):
        return any(role.id == ROLE_ID for role in ctx.author.roles)
    return False

class MyCommandTree(discord.app_commands.CommandTree):
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if isinstance(interaction.user, discord.Member):
            if any(role.id == ROLE_ID for role in interaction.user.roles):
                return True
        await interaction.response.send_message(
            "You do not have permission to use this command.",
            ephemeral=True
        )
        return False

bot = commands.Bot(
    command_prefix="9",
    intents=intents,
    tree_cls=MyCommandTree
)

bot.add_check(global_role_check)

@bot.event
async def on_ready():
    await bot.tree.sync()  # Global slash command sync (may take up to 1h for new cmds)
    print(f'Bot is online! Logged in as {bot.user}')

@bot.event
async def on_member_remove(member):
    # Don't act on bots
    if member.bot:
        return
    now = discord.utils.utcnow()
    joined = member.joined_at or now
    time_in = now - joined
    time_str = human_time_delta(time_in)
    channel_counts = {}
    try:
        for channel in member.guild.text_channels:
            count = 0
            try:
                async for msg in channel.history(limit=800, oldest_first=False):
                    if msg.author == member:
                        count += 1
                if count > 0:
                    channel_counts[channel.name] = count
            except (discord.Forbidden, discord.HTTPException):
                continue
    except Exception:
        channel_counts = {}

    details = [
        "<:v1:1396702889002401792><:v2:1396702906387796059><:v3:1396702922007515286>_**BANNED**_<:v1:1396702889002401792><:v2:1396702906387796059><:v3:1396702922007515286>",
        f"## **{member}** ({member.id})",
        f"Joined: ",
        f"Left: ",
        f"Stayed: {time_str}"
    ]
    if channel_counts:
        ch_reports = [f"{ch} - {cnt}msg" for ch, cnt in channel_counts.items()]
        details.append("Messages: " + "; ".join(ch_reports))
    else:
        details.append("Messages: none")

    details.append(
        "<:v1:1396702889002401792><:v2:1396702906387796059><:v2:1396702906387796059><:v2:1396702906387796059><:v2:1396702906387796059><:v3:1396702922007515286>"
    )
    report = "\n".join(details)
    log_channel = member.guild.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(report)
    try:
        await member.ban(reason="Auto-ban: user left the server.")
    except Exception as e:
        if log_channel:
            await log_channel.send(f"Failed to ban {member}: {e}")

@bot.command()
async def bulkban(ctx, *user_ids):
    banned = []
    failed = []
    for uid in user_ids:
        try:
            await ctx.guild.ban(discord.Object(id=int(uid)), reason="Bulk ban")
            banned.append(uid)
        except Exception as e:
            failed.append(f"{uid} ({e})")
    result = f"Banned: {', '.join(banned)}"
    if failed:
        result += f"\nFailed: {', '.join(failed)}"
    await ctx.send(result)

@bot.tree.command(name="bulkban", description="Ban multiple users by their IDs")
async def slash_bulkban(interaction: discord.Interaction, user_ids: str):
    ids = user_ids.split()
    banned = []
    failed = []
    for uid in ids:
        try:
            await interaction.guild.ban(discord.Object(id=int(uid)), reason="Bulk ban (slash command)")
            banned.append(uid)
        except Exception as e:
            failed.append(f"{uid} ({e})")
    reply = f"Banned: {', '.join(banned)}"
    if failed:
        reply += f"\nFailed: {', '.join(failed)}"
    await interaction.response.send_message(reply, ephemeral=True)

bot.run(TOKEN)
>>>>>>> 887ee7f4f65bf3584df20c9c543a8de3badc46ed
