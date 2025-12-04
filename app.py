import discord
import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_URL = "https://undetek.com/free-cs2-cheats-download/"  # لینک سایتی که باید کد رو بخونه
TARGET_DIV = "pin"  # id div که عدد داخلشه

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

def get_code():
    r = requests.get(TARGET_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    div = soup.find("div", {"id": TARGET_DIV})
    if div:
        return div.text.strip()
    return "❌ div پیدا نشد"

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.content.startswith("/code"):
        code = get_code()
        await message.channel.send(f"🔢 کد: **{code}**")

bot.run(TOKEN)
