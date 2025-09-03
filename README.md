Sync Proxy Harvester
====================

Author & Owner
--------------
- [heylzo](https://github.com/heylzo)

Contributors
------------
- [basam999](https://github.com/basam999)
- [Ryu-Dev-Here](https://github.com/Ryu-Dev-here)

Description
-----------
Sync Proxy Harvester is a Python tool that collects public SOCKS5 proxies 
from multiple sources, removes duplicates, checks which ones are alive, 
and saves the working proxies to simple text and json files.
It can also send the list automatically to a Discord channel.

Features
--------
- Fetch SOCKS5 proxies from multiple sources (socks5_sources.txt).
- Deduplicate and normalize proxy format.
- High-speed concurrent checking with configurable timeout.
- Save working proxies to:
  - live_proxies.txt
  - live_proxies.json
- Optional reporting to Discord channel with embeds.

Setup
-----
1. Install Python 3.11 or newer
2. Install dependencies:
   pip install -r req.txt
3. Copy .env.example to .env and set:
   DISCORD_BOT_TOKEN=your_bot_token
   DISCORD_CHANNEL_ID=your_channel_id
4. Run the script:
   python main.py

Files
-----
- main.py              main script
- req.txt              dependencies
- socks5_sources.txt   list of proxy sources
- .env.example         example environment config
- README.txt           project readme

License
-------
MIT License © 2025 heylzo, basam999, Ryu-Dev-Here
