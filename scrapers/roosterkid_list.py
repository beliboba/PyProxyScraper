import aiohttp

from utils.wtf import wtf

from rich import print
from rich.panel import Panel


class Info:
	name = "Roosterkid proxy list"
	supported_types = ["https", "socks4", "socks5"]
	scrape_type = "aiohttp"


async def scrape(output: str, ptype: str) -> list[str, int]:
	scraped = 0
	async with aiohttp.ClientSession() as session:
		ptype = "http" if ptype == "https" else ptype
		async with session.get(f"https://raw.githubusercontent.com/roosterkid/openproxylist/main/{ptype.capitalize()}_RAW.txt") as req:
			print(Panel.fit(f"[blue]Доступно прокси: {len((await req.text()).splitlines())}[/]"))
			for proxy in (await req.text()).splitlines():
				await wtf(output, proxy)
				scraped += 1
	return [Info.name, scraped]
