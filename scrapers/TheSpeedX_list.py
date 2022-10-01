import aiohttp
from utils.wtf import wtf


class Info:
	"""TheSpeedX list scraper"""

	name = "TheSpeedX list"
	supported_types = ["http", "https", "socks4", "socks5"]

	@staticmethod
	async def geturl(ptype: str):
		return f'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/{ptype}.txt'


async def scrape(output: str, ptype: str) -> None:
	"""Scrape TheSpeedX list"""
	async with aiohttp.ClientSession() as session:
		ptype = "http" if ptype == "https" else ptype
		async with session.get(await Info.geturl(ptype)) as req:
			for proxy in (await req.text()).splitlines():
				await wtf(output, proxy)
