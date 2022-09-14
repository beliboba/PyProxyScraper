import asyncio
import os
import inspect
import sys
from os.path import isfile

from rich import print
from rich.panel import Panel

import scrapers


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.headless = True
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


async def menu():
	print(Panel.fit("[blue bold]Выберите тип прокси для скрапинга:[/]\n1. http\n2. https\n3. socks4\n4. socks5 \n [blue bold]Введите цифру[/]"))
	types = {
		1: "http",
		2: "https",
		3: "socks4",
		4: "socks5"
	}
	ptype = types[int(input())]
	print(Panel.fit("[yellow bold]Введите файл для вывода[/]"))
	output = input()
	for scraper in get_scrapers():
		if ptype in scraper.Info.supported_types and scraper.Info.name:
			if scraper.Info.scrape_type == "selenium":
				print(Panel.fit(f"[blue bold]{scraper.Info.name}[/]"))
				scr = await scraper.scrape(output, ptype, driver)
				print(Panel.fit(f"[blue]{scr[0]}[/][green]Scraped: {scr[1]}[/]"))
			elif scraper.Info.scrape_type == "aiohttp":
				print(Panel.fit(f"[blue bold]{scraper.Info.name}[/]"))
				scr = await scraper.scrape(output, ptype)
				print(Panel.fit(f"[blue]{scr[0]}[/][green]Scraped: {scr[1]}[/]"))
			else:
				print(Panel.fit(f"[red] Ошибка! Скрапер {scraper.Info.name} имеет неправильную конфигурацию!"))


def get_scrapers():
	sys.path.insert(0, './scrapers')
	return [__import__(file.replace(".py", "")) for file in os.listdir('./scrapers') if file.endswith(".py")]


if __name__ == "__main__":
	asyncio.run(menu())
