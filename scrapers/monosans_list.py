import aiohttp
from utils.wtf import wtf


class Info:
	"""Monosans list scraper"""

	name = "Monosans proxy list"
	supported_types = ["http", "socks4", "socks5"]

	@staticmethod
	async def geturl(ptype: str):
		return f"https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/{ptype}.txt"


async def scrape(output: str, ptype: str) -> None:
	"""Scrape Monosans proxy list"""
	async with aiohttp.ClientSession() as session:
		async with session.get(await Info.geturl(ptype)) as req:
			for proxy in (await req.text()).splitlines():
				await wtf(output, proxy)
