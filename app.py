import os
import discord
from discord.ext import commands
from aiohttp import web
import aiohttp
import re
import asyncio

# -------------------------------
# تنظیمات سایت
# -------------------------------
TARGET_URL = "https://example.com/page"   # آدرس سایت
TARGET_DIV_ID = "myDivId"                 # ID div
# -------------------------------

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


async def fetch_div_value():
    """برداشتن مقدار div از سایت"""
    async with aiohttp.ClientSession() as session:
        async with session.get(TARGET_URL, headers={"User-Agent": "DiscordBot/1.0"}) as resp:
            if resp.status != 200:
                return f"خطا در دریافت سایت: {resp.status}"

            html = await resp.text()

    safe_id = re.escape(TARGET_DIV_ID)
    pattern = rf'<div[^>]+id=["\']{safe_id}["\'][^>]*>(.*?)</div>'
    match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)

    if not match:
        return "div موردنظر پیدا نشد!"

    text = re.sub(r"<[^>]+>", "", match.group(1)).strip()
    return text if text else "div خالی بود"


@bot.command()
async def code(ctx):
    """!code → مقدار div را می‌گیرد"""
    await ctx.send("⏳ در حال دریافت...")
    result = await fetch_div_value()
    await ctx.send(f"📌 نتیجه:\n`{result}`")


# -------------------------------
# وب‌سرور کوچک برای UptimeRobot
# -------------------------------
async def handle(request):
    return web.Response(text="Bot is alive")

app = web.Application()
app.router.add_get("/", handle)

# -------------------------------
# اجرای همزمان Bot + WebServer
# -------------------------------
async def main():
    loop = asyncio.get_running_loop()

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 10000)))
    await site.start()

    print("Web server started")

    await bot.start(TOKEN)


asyncio.run(main())
