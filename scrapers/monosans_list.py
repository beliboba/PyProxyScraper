import aiohttp
from utils.wtf import wtf


class Info:
	name = "Monosans proxy list"
	supported_types = ["http", "socks4", "socks5"]


async def scrape(output: str, ptype: str) -> None:
	async with aiohttp.ClientSession() as session:
		async with session.get(f"https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/{ptype}.txt") as req:
			for proxy in (await req.text()).splitlines():
				await wtf(output, proxy)
