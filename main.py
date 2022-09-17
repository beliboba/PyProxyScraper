import asyncio
import os
import sys

from rich import print
from rich.panel import Panel


async def menu():
	ptypes = ['http', 'https', 'socks4', 'socks5']
	for ptype in ptypes:
		await scrape(ptype)
		print(Panel.fit(f"[green]Done[/]"))


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
