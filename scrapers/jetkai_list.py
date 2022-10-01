import aiohttp
from utils.wtf import wtf


class Info:
	"""Jetkai list scraper"""

	name = "Jetkai proxy list"
	supported_types = ["http", "socks4", "socks5"]

	@staticmethod
	async def geturl(ptype: str):
		return f"https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-{ptype}.txt"


async def scrape(output: str, ptype: str) -> None:
	"""Scrape Jetkai proxy list"""
	async with aiohttp.ClientSession() as session:
		async with session.get(await Info.geturl(ptype)) as req:
			for proxy in (await req.text()).splitlines():
				await wtf(output, proxy)
