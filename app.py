import os
import discord
import cloudscraper
from bs4 import BeautifulSoup
from aiohttp import web
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")

# URL و div واقعی
TARGET_URL = "https://undetek.com/free-cs2-cheats-download/"
TARGET_DIV_ID = "getpin"

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

# Scraper که Cloudflare را دور می‌زند
scraper = cloudscraper.create_scraper()

def get_pin():
    try:
        html = scraper.get(TARGET_URL).text
        soup = BeautifulSoup(html, "html.parser")
        div = soup.find("div", {"id": TARGET_DIV_ID})
        if div:
            return div.text.strip()

        return "❌ div پیدا نشد (getpin)"

    except Exception as e:
        return f"❌ خطا: {e}"

@bot.event
async def on_ready():
    print(f"Bot آنلاین شد: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("/code"):
        pin = get_pin()
        await message.channel.send(f"🔢 پین سایت: **{pin}**")


# ---------- Web Server برای UptimeRobot ----------
async def handle(request):
    return web.Response(text="Bot Alive!")

app = web.Application()
app.router.add_get("/", handle)

async def main():
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print("Keep-alive server running")

    await bot.start(TOKEN)

asyncio.run(main())
