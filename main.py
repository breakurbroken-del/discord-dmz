import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# Default Settings (Bot on hole egulo thakbe)
config = {
    "normal_msg": "Hey {user}, check this out!",
    "embed_title": "Default Title",
    "embed_desc": "Default Description",
    "image_url": "https://i.imgur.com/example.png",
    "hex_color": 0x3498db,
    "locked_guild_id": None # Ekhane tomar server ID thakbe
}

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True # Command porar jonno dorkar

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} is online!')

# 1. Command: Message Customize Kora
@bot.command()
async def setmsg(ctx, title, desc, img, color_hex):
    global config
    config["embed_title"] = title
    config["embed_desc"] = desc
    config["image_url"] = img
    config["hex_color"] = int(color_hex.replace("#", ""), 16)
    await ctx.send("✅ Message settings updated successfully!")

# 2. Command: Server Lock Kora (Jate ei server theke leave na kore)
@bot.command()
async def lock(ctx):
    global config
    config["locked_guild_id"] = ctx.guild.id
    await ctx.send(f"🔒 Bot is now locked to **{ctx.guild.name}**. It won't leave this server!")

# --- Auto Task on Join ---
@bot.event
async def on_guild_join(guild):
    # Check kora server ta lock kora kina
    if guild.id == config["locked_guild_id"]:
        print(f"Joined locked server {guild.name}. Staying here.")
        return

    print(f"Joined new server: {guild.name}. Starting task...")
    
    embed = discord.Embed(
        title=config["embed_title"], 
        description=config["embed_desc"], 
        color=config["hex_color"]
    )
    embed.set_image(url=config["image_url"])
    
    count = 0
    async for member in guild.fetch_members(limit=100):
        if not member.bot and count < 5:
            try:
                mention_msg = config["normal_msg"].format(user=member.mention)
                await member.send(mention_msg)
                await member.send(embed=embed)
                count += 1
                await asyncio.sleep(2)
            except:
                continue

    print(f"Task done. Leaving {guild.name}...")
    await guild.leave()

bot.run(TOKEN)
