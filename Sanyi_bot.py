import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bejelentkezve mint: {bot.user}")

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
