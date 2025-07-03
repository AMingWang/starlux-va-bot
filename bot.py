import discord
from discord.ext import commands, tasks
import os
import random
import requests
from datetime import datetime

# 環境變數
TOKEN = os.getenv("MTM4OTk4MjI1NzAxMTIzMjgxOA.GtqnFd.3goXet3X63TcYzYZsXuCHnCg_85by8mEmoplq0")
GUILD_ID = int(os.getenv("1279296034945896471", "0"))
ANNOUNCE_CHANNEL_ID = int(os.getenv("1307623989774123008", "0"))
AVWX_TOKEN = os.getenv("AVWX_TOKEN")

# Discord Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 任務清單
missions = [
    "模擬 RCTP-VHHH 貨運航班，執行 RNAV 進場",
    "從 RJAA 飛至 RCTP，模擬ILS CAT II進場，側風 12 節",
    "從 RCTP 起飛後模擬單發操作備降至 RCSS",
    "執行 RPLL-RCTP 客運航班，模擬油量偏低情境"
]

@bot.event
async def on_ready():
    print(f"✅ BOT 已上線：{bot.user}")
    daily_announce.start()

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong! BOT 正常運作中。")

@bot.command()
async def verify(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="飛行員")
    if role:
        await member.add_roles(role)
        await ctx.send(f"✅ 已給予 {member.mention} 飛行員身分組！")
    else:
        await ctx.send("⚠️ 找不到 '飛行員' 身分組，請先建立。")

@bot.command()
async def announce(ctx, *, msg):
    channel = bot.get_channel(ANNOUNCE_CHANNEL_ID)
    if channel:
        await channel.send(f"📢 **航班公告**\n{msg}")
        await ctx.send("✅ 已發佈公告。")
    else:
        await ctx.send("❌ 找不到公告頻道。")

@bot.command()
async def mission(ctx):
    selected = random.choice(missions)
    await ctx.send(f"✈️ 今日隨機任務：{selected}")

@bot.command()
async def metar(ctx, icao):
    try:
        response = requests.get(
            f"https://avwx.rest/api/metar/{icao}?token={AVWX_TOKEN}"
        )
        if response.status_code == 200:
            data = response.json()
            await ctx.send(f"📡 {icao.upper()} METAR：{data['raw']}")
        else:
            await ctx.send("❌ 無法取得 METAR 資料。")
    except Exception:
        await ctx.send("⚠️ 查詢失敗。")

@tasks.loop(minutes=60)
async def daily_announce():
    now = datetime.now()
    if now.hour == 18:
        channel = bot.get_channel(ANNOUNCE_CHANNEL_ID)
        if channel:
            await channel.send("⭐ 提醒：明天 RCTP - RJTT 集體飛行，請提前準備！")

bot.run(TOKEN)
