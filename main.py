import asyncio
import os
import sys
import argparse


async def menu():
	for scraper in get_scrapers():
		if ptype in scraper.Info.supported_types and scraper.Info.name:
			await scraper.scrape(output, ptype)


def get_scrapers():
	sys.path.insert(0, './scrapers')
	return [__import__(file.replace(".py", "")) for file in os.listdir('./scrapers') if file.endswith(".py")]


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Proxy scraper')
	parser.add_argument('-o', '--output', help='Output file', required=True)
	parser.add_argument('-t', '--type', help='Proxy type', required=True)
	args = parser.parse_args()
	output = args.output
	ptype = args.type
	asyncio.run(menu())
