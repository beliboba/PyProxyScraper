import asyncio
import os
import sys

from rich import print
from rich.panel import Panel


async def menu():
	ptypes = ['http', 'https', 'socks4', 'socks5']
	for ptype in ptypes:
		output = f'./proxies/{ptype}.txt'
		for scraper in get_scrapers():
			if ptype in scraper.Info.supported_types and scraper.Info.name:
				print(Panel.fit(f"[blue bold]{scraper.Info.name}[/]"))
				scr = await scraper.scrape(output, ptype)
				print(Panel.fit(f"[blue]{scr[0]}[/][green]Scraped: {scr[1]}[/]"))


def get_scrapers():
	sys.path.insert(0, './scrapers')
	return [__import__(file.replace(".py", "")) for file in os.listdir('./scrapers') if file.endswith(".py")]


if __name__ == "__main__":
	asyncio.run(menu())
