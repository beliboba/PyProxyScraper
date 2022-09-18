import aiohttp
from utils.wtf import wtf


class Info:
	name = "Roosterkid proxy list"
	supported_types = ["https", "socks4", "socks5"]


async def scrape(output: str, ptype: str) -> None:
	async with aiohttp.ClientSession() as session:
		ptype = "http" if ptype == "https" else ptype
		async with session.get(f"https://raw.githubusercontent.com/roosterkid/openproxylist/main/{ptype.capitalize()}_RAW.txt") as req:
			for proxy in (await req.text()).splitlines():
				await wtf(output, proxy)
