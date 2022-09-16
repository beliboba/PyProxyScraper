import aiohttp

from utils.wtf import wtf
from utils.clear import clear

from rich import print
from rich.panel import Panel


class Info:
	name = "Geonode"
	supported_types = ["http", "https", "socks4", "socks5"]


async def scrape(output: str, ptype: str) -> list[str, int]:
	if ptype in Info.supported_types:
		async with aiohttp.ClientSession() as session:
			async with session.get(f'https://proxylist.geonode.com/api/proxy-list?limit=0&page=1&sort_by=lastChecked&sort_type=desc&protocols={ptype}') as response:
				print(Panel.fit(f"[green]Доступно {response.json['total']} прокси[/]"))
				proxies = response.json['data']
				scraped = 0
				for proxy in proxies:
					ip = proxy['ip']
					port = proxy['port']
					await wtf(output, f"{ip}:{port}")
					scraped += 1
					clear()
	return [Info.name, scraped]
