import os

import aiofiles
import aiohttp

from rich import print
from rich.panel import Panel


class Info:
	name = "Geonode"
	supported_types = ["http", "https", "socks4", "socks5"]


async def scrape(output: str, ptype: str):
	async with aiohttp.ClientSession() as session:
		async with session.get(f'https://proxylist.geonode.com/api/proxy-list?limit=0&page=1&sort_by=lastChecked&sort_type=desc&protocols={ptype}') as response:
			print(Panel.fit(f"[green]Доступно {response.json['total']} прокси[/]"))
			proxies = response.json['data']
			scraped = 0
			for proxy in proxies:
				ip = proxy['ip']
				port = proxy['port']
				async with aiofiles.open(output, 'a+') as f:
					if f"{ip}:{port}" not in await f.readlines():
						await f.write(f"{ip}:{port}\n")
				scraped += 1
				print(Panel.fit(f"[green bold]{scraped}[/]"))
				os.system("clear | cls")
				print(Panel.fit(f"[blue bold]Geonode[/]\n[blue]Доступно прокси: {len(proxies)}[/]\n[green]Scraped: {scraped}[/]"))