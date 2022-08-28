import os

import aiofiles
import aiohttp

from utils.wtf import wtf
from utils.clear import clear

from rich import print
from rich.panel import Panel


class Info:
	name = "OpenProxyList"
	supported_types = ["http", "https", "socks4", "socks5"]
	scrape_type = "aiohttp"


async def scrape(output: str, ptype: str):
	if ptype in Info.supported_types:
		scraped = 0
		async with aiohttp.ClientSession() as session:
			ptype = "http" if ptype == "https" else ptype
			async with session.get(f'https://openproxylist.xyz/{ptype}.txt') as req:
				print(Panel.fit(f"[blue]Доступно прокси: {len((await req.text()).splitlines())}[/]"))
				for proxy in (await req.text()).splitlines():
					await wtf(output, proxy)
					scraped += 1
		print(Panel.fit(f"[green]Scraped: {scraped}[/]"))
