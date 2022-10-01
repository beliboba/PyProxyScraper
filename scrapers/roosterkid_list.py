import aiohttp
from utils.wtf import wtf


class Info:
	"""RoosterKid list scraper"""

	name = "Roosterkid proxy list"
	supported_types = ["https", "socks4", "socks5"]

	@staticmethod
	async def geturl(ptype: str):
		return f"https://raw.githubusercontent.com/roosterkid/openproxylist/main/{ptype.capitalize()}_RAW.txt"


async def scrape(output: str, ptype: str) -> None:
	"""Scrape Roosterkid proxy list"""
	async with aiohttp.ClientSession() as session:
		ptype = "http" if ptype == "https" else ptype
		async with session.get(await Info.geturl(ptype)) as req:
			for proxy in (await req.text()).splitlines():
				await wtf(output, proxy)
