Lzo Proxy Harvester
===================

Author: heylzo (https://github.com/heylzo)

This is a small Python tool that collects public SOCKS5 proxies from a list of sources,
checks which ones are alive, and saves the results to simple text and json files.
It can also send the list to a Discord channel.

How it works
------------
- Reads sources from socks5_sources.txt
- Downloads and merges all proxies
- Removes duplicates
- Checks each proxy with a quick timeout
- Saves working proxies to live_proxies.txt and live_proxies.json
- Optionally posts the results to Discord

Setup
-----
1. Install Python 3.11 or newer
2. Install dependencies:
   pip install -r req.txt
3. Copy .env.example to .env and set your Discord bot token and channel id
4. Run:
   python main.py

Files
-----
- main.py              main script
- req.txt              requirements
- socks5_sources.txt   list of proxy sources
- .env.example         example environment config

License
-------
MIT License © 2025 heylzo
