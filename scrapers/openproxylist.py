import aiohttp
from utils.wtf import wtf


class Info:
	"""OpenProxyList scraper"""

	name = "OpenProxyList"
	supported_types = ["http", "https", "socks4", "socks5"]

	@staticmethod
	async def geturl(ptype: str):
		return f'https://openproxylist.xyz/{ptype}.txt'


async def scrape(output: str, ptype: str) -> None:
	"""Scrape OpenProxyList"""
	async with aiohttp.ClientSession() as session:
		ptype = "http" if ptype == "https" else ptype
		async with session.get(await Info.geturl(ptype)) as req:
			for proxy in (await req.text()).splitlines():
				await wtf(output, proxy)
