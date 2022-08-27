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
	print(Panel.fit(f"[blue bold]Выберите тип прокси для скрапинга:[/]\n1. http\n2. https\n3. socks4\n4. socks5 \n [blue bold]Введите цифру[/]"))
	types = {
		1: "http",
		2: "https",
		3: "socks4",
		4: "socks5"
	}
	ptype = types[int(input())]
	print(Panel.fit("[yellow bold]Введите файл для вывода[/]"))
	output = input()
	if not isfile(output):
		print(Panel.fit(f"[red] Ошибка! '{output}' - не файл!"))
		os.abort()
	scrapers = get_scrapers()
	#for scraper in scrapers:
	#	if ptype in scraper.Info.supported_types:
	#		await scraper.scrape()


def get_scrapers():
	files = os.listdir('./scrapers')
	sys.path.insert(0, './scrapers')
	loaded_services = []

	for file in files:
		if file.endswith(".py"):
			module = __import__(file.replace(".py", ""))
			loaded_services.append(module)
	return loaded_services  # TODO: Convert to a list comprehension


if __name__ == "__main__":
	asyncio.run(menu())
