# Sync Proxy Harvester
# Author: heylzo (https://github.com/heylzo)
# Contributors: basam999, Ryu-Dev-Here
# License: MIT
# Initial Release 2025
import os
import socket
import asyncio
import discord
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init

init(autoreset=True)

# === CONFIG ===
MAX_THREADS = 1500
TIMEOUT = 1.5
SLEEP_SECONDS = 45 * 60  # 45 minutes
PROXY_SOURCES_FILE = "socks5_sources.txt"
OUTPUT_FILE = "live_proxies.txt"
JSON_OUTPUT = "live_proxies.json"
SCAN_TIMEOUT = 1800

DEFAULT_URLS = [
    "https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/refs/heads/main/socks5.txt",
    "https://raw.githubusercontent.com/databay-labs/free-proxy-list/refs/heads/master/socks5.txt",
    "https://raw.githubusercontent.com/ebrasha/abdal-proxy-hub/refs/heads/main/socks5-proxy-list-by-EbraSha.txt",
    "https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/protocols/socks5/data.txt",
    "https://raw.githubusercontent.com/handeveloper1/Proxy/refs/heads/main/Proxies-Ercin/socks5.txt",
    "https://raw.githubusercontent.com/casa-ls/proxy-list/refs/heads/main/socks5",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/refs/heads/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/FifzzSENZE/Master-Proxy/refs/heads/master/proxies/socks5.txt",
    "https://raw.githubusercontent.com/zebbern/Proxy-Scraper/refs/heads/main/socks5.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/socks5.txt",
    "https://raw.githubusercontent.com/trio666/proxy-checker/refs/heads/main/socks5.txt",
    "https://raw.githubusercontent.com/RioMMO/ProxyFree/refs/heads/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/iplocate/free-proxy-list/refs/heads/main/protocols/socks5.txt",
    "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/socks5.txt",
    "https://raw.githubusercontent.com/dinoz0rg/proxy-list/refs/heads/main/scraped_proxies/socks5.txt"
]

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)


def ensure_sources_file():
    if not os.path.exists(PROXY_SOURCES_FILE):
        with open(PROXY_SOURCES_FILE, "w") as f:
            f.write("\n".join(DEFAULT_URLS))


def fetch_all_proxies():
    ensure_sources_file()
    proxies = set()
    with open(PROXY_SOURCES_FILE, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        try:
            res = requests.get(url, timeout=10)
            for line in res.text.strip().splitlines():
                if ":" in line and line.count(":") == 1:
                    proxies.add(line.strip())
            print(Fore.GREEN + f"[+] {url} => {len(proxies)} total")
        except Exception as e:
            print(Fore.RED + f"[ERROR] Failed to fetch {url}: {e}")
    return list(proxies)


def check_socks5_proxy(proxy):
    try:
        ip, port = proxy.split(":")
        start = datetime.now()
        with socket.create_connection((ip, int(port)), timeout=TIMEOUT):
            latency = (datetime.now() - start).total_seconds() * 1000
        geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=2).json()
        country = geo.get("country", "Unknown")
        city = geo.get("city", "Unknown")
        return {"proxy": proxy, "ping": round(latency), "country": country, "city": city}
    except:
        return None


def run_proxy_scan(proxies):
    results = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(check_socks5_proxy, proxy): proxy for proxy in proxies}
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    return results


async def send_result_to_discord(results):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if not channel:
        print(Fore.RED + "[ERROR] Discord channel not found.")
        return

    with open(OUTPUT_FILE, "w") as f:
        for r in results:
            f.write(r["proxy"] + "\n")

    with open(JSON_OUTPUT, "w") as f:
        json.dump(results, f, indent=2)

    embed = discord.Embed(
        title="ProxyCloner Edition — Live Proxies",
        description=f"**Live Proxies:** `{len(results)}`\n📦 JSON + TXT attached\n🕓 `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
        color=discord.Color.green()
    )
    embed.set_footer(text="Powered by ProxyCloner Edition")
    embed.timestamp = datetime.now()
    await channel.send(embed=embed)
    await channel.send(file=discord.File(OUTPUT_FILE))
    await channel.send(file=discord.File(JSON_OUTPUT))


async def run_single_cycle():
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if not channel:
        return

    embed_start = discord.Embed(
        title="ProxyCloner",
        description="**Starting proxy fetch...**",
        color=discord.Color.blue()
    )
    embed_start.set_footer(text="Proxy Engine Initialized")
    embed_start.timestamp = datetime.now()
    await channel.send(embed=embed_start)

    all_proxies = await asyncio.to_thread(fetch_all_proxies)

    embed_fetch = discord.Embed(
        title="🔍 Verifying Proxies",
        description=f"Fetched: `{len(all_proxies)}` SOCKS5 proxies\nBeginning verification phase...",
        color=discord.Color.orange()
    )
    embed_fetch.timestamp = datetime.now()
    await channel.send(embed=embed_fetch)

    results = await asyncio.to_thread(run_proxy_scan, all_proxies)

    embed_verify = discord.Embed(
        title="📦 Packing Live Proxies",
        description=f"Found `{len(results)}` working proxies with ping + geo.",
        color=discord.Color.teal()
    )
    embed_verify.timestamp = datetime.now()
    await channel.send(embed=embed_verify)

    if results:
        await send_result_to_discord(results)


@bot.event
async def on_ready():
    print(Fore.MAGENTA + f"[+] Bot connected as {bot.user}")
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        boot_embed = discord.Embed(
            title="🤖 ProxyCloner Online",
            description="Bot is online and scanning every 45 minutes.",
            color=discord.Color.purple()
        )
        boot_embed.timestamp = datetime.now()
        boot_embed.set_footer(text="Session Active | ProxyCloner")
        await channel.send(embed=boot_embed)

    while True:
        try:
            await asyncio.wait_for(run_single_cycle(), timeout=SCAN_TIMEOUT)
        except asyncio.TimeoutError:
            await send_embed(channel, "❌ Timeout", "Scan took too long and timed out!", discord.Color.red())
        except Exception as e:
            await send_embed(channel, "⚠️ Error", f"Unhandled error:\n```{str(e)}```", discord.Color.red())

        sleep_embed = discord.Embed(
            title="😴 Sleeping",
            description=f"Next cycle in **{SLEEP_SECONDS // 60} minutes**...",
            color=discord.Color.dark_gray()
        )
        sleep_embed.timestamp = datetime.now()
        await channel.send(embed=sleep_embed)

        await asyncio.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
