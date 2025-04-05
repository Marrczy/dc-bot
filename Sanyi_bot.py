import os
import discord
from discord.ext import commands
import requests
import time
import psutil
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = "https://cheat-collection-qualities-opposite.trycloudflare.com/start-server"
API_SECRET = "Fuq/Ak6Xm#uq?7xwW0vx20as:UtiGk)Q6m£*(xS%/.8B#Vi8,%"

scheduler = AsyncIOScheduler()
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bejelentkezve mint: {bot.user}")
    scheduler.add_job(auto_backup, CronTrigger(hour=22, minute=0))
    scheduler.start()

def is_java_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'java' in proc.info['name'].lower():
            return True
    return False

async def auto_backup():
    channel = bot.get_channel(1358096800686281047)
    if channel:
        await channel.send("🕓 Automatikus backup indult (22:00)")

    if is_java_running():
        if channel:
            await channel.send("🔻 Szerver fut – leállítás...")
        subprocess.run(["taskkill", "/IM", "java.exe", "/F"])
        await channel.send("⏳ Várakozás 60 mp a teljes leálláshoz...")
        time.sleep(60)
    else:
        if channel:
            await channel.send("ℹ️ A szerver már le volt állítva – nem kell leállítani.")

    subprocess.run(["python", "C:\\Users\\koppa\\Documents\\Scripts\\minecraft_backup.py"])

    if channel:
        await channel.send("✅ Backup kész! A mentés az iCloud Drive-ban van.")

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="🤖 Sanyi – WithTheBoys Discord Bot",
        description="Itt van minden parancsom és funkcióm!",
        color=0x57F287
    )

    embed.add_field(
        name="📦 !backup",
        value="Leállítja a szervert (ha fut), majd biztonsági mentést készít és menti iCloud Drive-ba.",
        inline=False
    )

    embed.add_field(
        name="🕓 Automatikus mentés",
        value="Minden nap **22:00-kor** automatikusan biztonsági mentést indít.",
        inline=False
    )

    embed.add_field(
        name="🛑 !stop",
        value="Leállítja a botot (csak tulaj használhatja).",
        inline=False
    )

    embed.add_field(
        name="🧩 !mod",
        value="Link a modpack telepítőhöz (.exe formában).",
        inline=False
    )

    embed.add_field(
        name="📜 !modlist",
        value="Felsorolja a modokat, amik a szerveren futnak.",
        inline=False
    )

    embed.set_footer(text="WithTheBoys Minecraft Szerver bot – Powered by Sanyi 😼")

    await ctx.send(embed=embed)

@bot.command()
async def backup(ctx):
    if ctx.author.id != 396322349236092930:
        await ctx.send("🚫 Csak a tulaj használhatja ezt a parancsot.")
        return

    await ctx.send("🔄 Manuális backup indítása...")

    if is_java_running():
        await ctx.send("🔻 Szerver fut – leállítás...")
        subprocess.run(["taskkill", "/IM", "java.exe", "/F"])
        await ctx.send("⏳ Várakozás 60 mp a teljes leálláshoz...")
        time.sleep(60)
    else:
        await ctx.send("ℹ️ A szerver már le volt állítva – nem kell leállítani.")

    subprocess.run(["python", "C:\\Users\\koppa\\Documents\\Scripts\\minecraft_backup.py"])
    await ctx.send("✅ Backup kész!")


@bot.command(name="szerverstatus")
async def szerverstatus(ctx):
    await ctx.send("🔎 Lekérdezem a szerver állapotát...")

    try:
        response = requests.get(API_URL.replace("/start-server", "/server-status"))
        data = response.json()

        if data["status"] == "running":
            await ctx.send("🟢 A Minecraft szerver **fut**.")
        elif data["status"] == "stopped":
            await ctx.send("🔴 A Minecraft szerver **nem fut**.")
        else:
            await ctx.send(f"⚠️ Ismeretlen válasz: {data['message']}")
    except Exception as e:
        await ctx.send(f"❌ Hiba történt: {str(e)}")

@bot.command(name="szerverstart")
async def szerverstart(ctx):
    await ctx.send("🔄 Indítom a Minecraft szervert...")

    headers = {"Authorization": API_SECRET}

    try:
        response = requests.post(API_URL, headers=headers)
        data = response.json()

        if data["status"] == "success":
            await ctx.send("✅ Szerver elindítva!")
        elif data["status"] == "info":
            await ctx.send("ℹ️ A szerver már fut!")
        else:
            await ctx.send(f"❌ Hiba: {data['message']}")
    except Exception as e:
        await ctx.send(f"⚠️ Hiba történt: {str(e)}")

@bot.command(name="modlist")
async def modlist(ctx):
    await ctx.send("🧩 Jelenlegi modok: BetterFPS, Sodium, stb...")

@bot.command(name="mod")
async def telepito(ctx):
    embed = discord.Embed(
        title="🔧 Minecraft Modpack Telepítő",
        description="Töltsd le a modpack telepítőt az alábbi linkről:",
        color=0x57F287
    )
    embed.add_field(
        name="📦 Letöltés:",
        value="[mods_install.exe – Dropbox link](https://www.dropbox.com/scl/fi/nyvqmw2qk4n43holf8qdj/ModInstaller.zip?rlkey=34jvuboobguwnhczqavla97tp&st=tn64r23t&dl=1)",
        inline=False
    )
    await ctx.send(embed=embed)

@bot.command(name="stop")
async def stopping_bot(ctx):
    if ctx.author.id != 396322349236092930:
        await ctx.send("🚫 Ezt csak a bot tulajdonosa használhatja.")
        return

    await ctx.send("👋 Bot leáll... Viszlát!")
    await bot.close()

bot.run(TOKEN)
