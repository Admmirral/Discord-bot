import os
import discord
from discord.ext import commands
import aiohttp
import re

# ------------------------------
# تنظیمات
# ------------------------------
TARGET_URL = "https://example.com/page"   # آدرس صفحه
TARGET_DIV_ID = "myDivId"                 # ID همان div
# ------------------------------

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

    # Regex پیدا کردن div
    safe_id = re.escape(TARGET_DIV_ID)
    pattern = rf'<div[^>]+id=["\']{safe_id}["\'][^>]*>(.*?)</div>'
    match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)

    if not match:
        return "div موردنظر پیدا نشد!"

    # پاک کردن تگ‌های HTML
    text = re.sub(r"<[^>]+>", "", match.group(1)).strip()

    return text if text else "div خالی بود"


@bot.command()
async def code(ctx):
    """دستور !code"""
    await ctx.send("⏳ در حال دریافت اطلاعات...")
    result = await fetch_div_value()
    await ctx.send(f"📌 نتیجه:\n`{result}`")


bot.run(TOKEN)
