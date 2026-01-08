import os
import requests
import discord
from discord.ext import commands

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
N8N_WEBHOOK_URL = "https://IP:PORT/webhook/discord-plan"  

INTENTS = discord.Intents.default()
INTENTS.message_content = True  

bot = commands.Bot(command_prefix="!", intents=INTENTS)

@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user} (ID: {bot.user.id})")

@bot.command(name="plan")
async def plan(ctx, *, content: str):
    payload = {
        "mode": "plan",
        "channel_id": ctx.channel.id,
        "user": str(ctx.author),
        "content": content,
    }
    requests.post(N8N_WEBHOOK_URL, json=payload)
    await ctx.send("Tworzę plan na podstawie tej wiadomości…")

@bot.command(name="dzisiaj")
async def dzisiaj(ctx):
    payload = {
        "mode": "today",
        "channel_id": ctx.channel.id,
        "user": str(ctx.author),
    }
    requests.post(N8N_WEBHOOK_URL, json=payload)
    await ctx.send("Zbieram zadania na dzisiaj…")

@bot.command(name="jutro")
async def jutro(ctx):
    payload = {
        "mode": "tomorrow",
        "channel_id": ctx.channel.id,
        "user": str(ctx.author),
    }
    requests.post(N8N_WEBHOOK_URL, json=payload)
    await ctx.send("Zbieram zadania na jutro…")

@bot.command(name="dzien")
async def dzien(ctx, date_iso: str):
    payload = {
        "mode": "by_date",
        "channel_id": ctx.channel.id,
        "user": str(ctx.author),
        "date": date_iso,  
    }
    requests.post(N8N_WEBHOOK_URL, json=payload)
    await ctx.send(f"Zbieram zadania na {date_iso}…")

@bot.command(name="zmien")
async def zmien(ctx, *, text: str):
    payload = {
        "mode": "agent_update",
        "channel_id": ctx.channel.id,
        "user": str(ctx.author),
        "content": text,
    }
    requests.post(N8N_WEBHOOK_URL, json=payload)
    await ctx.send("Myślę nad zmianą planu…")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
