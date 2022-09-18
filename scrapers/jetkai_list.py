import aiohttp
from utils.wtf import wtf


class Info:
	name = "Jetkai proxy list"
	supported_types = ["http", "socks4", "socks5"]


async def scrape(output: str, ptype: str) -> None:
	async with aiohttp.ClientSession() as session:
		async with session.get(f"https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-{ptype}.txt") as req:
			for proxy in (await req.text()).splitlines():
				await wtf(output, proxy)
