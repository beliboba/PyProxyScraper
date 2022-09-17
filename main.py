import asyncio
import os
import sys

from rich import print
from rich.panel import Panel


async def menu():
	await scrape('http')
	await scrape('https')
	await scrape('socks4')
	await scrape('socks5')


async def scrape(ptype: str):
	output = f'./proxies/{ptype}.txt'
	for scraper in get_scrapers():
		if ptype in scraper.Info.supported_types and scraper.Info.name:
			await scraper.scrape(output, ptype)


def get_scrapers():
	sys.path.insert(0, './scrapers')
	return [__import__(file.replace(".py", "")) for file in os.listdir('./scrapers') if file.endswith(".py")]


if __name__ == "__main__":
	asyncio.run(menu())
