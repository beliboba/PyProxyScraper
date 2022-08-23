import os
import sys

import aiofiles
import asyncio

import aiohttp
from rich import print
from rich.panel import Panel

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.headless = True
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


async def hmn_scrape(output: str, ptype: str) -> None:
	driver.get('https://hidemy.name/ru/proxy-list/')
	paginator = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[5]/ul")
	pages = paginator.find_element(By.CSS_SELECTOR, "ul > li:nth-last-child(2)")
	pagecount = int(pages.find_element(By.TAG_NAME, 'a').text)
	scraped = 0
	types = {"http": "h", "https": "s", "socks4": "4", "socks5": "5"}
	for i in range(pagecount):
		print(Panel.fit(f"[blue bold]Страница: {i}[/]"))
		driver.get(f'https://hidemy.name/ru/proxy-list/?type={types[ptype]}&start={i*64}#list')
		rows = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[4]/table/tbody")
		for proxyrow in rows.find_elements(By.TAG_NAME, 'tr'):
			ip = proxyrow.find_element(By.CSS_SELECTOR, "tr > td:nth-child(1)").get_attribute("innerHTML")
			port = proxyrow.find_element(By.CSS_SELECTOR, "tr > td:nth-child(2)").get_attribute("innerHTML")
			async with aiofiles.open(output, 'a+') as f:
				if f"{ip}:{port}" not in await f.readlines():
					await f.write(f"{ip}:{port}\n")
			scraped += 1
			os.system("clear | cls")
			print(Panel.fit(f"[blue bold]HideMyName[/]\n[blue]Доступно прокси: {pagecount * 64}[/]\n[green]Scraped: {scraped}[/]"))


async def fplist_scrape(output: str, ptype: str) -> None:
	supported_types = ["http", "https"]
	types = {
		"http": "no",
		"https": "yes"
	}
	scraped = 0
	if ptype not in supported_types:
		print(Panel.fit(f"[red]Неподдерживаемый тип прокси. Поддерживаемые типы: http, https[/]"))
		sys.exit(1)
	driver.get('https://free-proxy-list.net/')
	rows = driver.find_element(By.XPATH, "//*[@id='list']/div/div[2]/div/table/tbody").find_elements(By.TAG_NAME, 'tr')
	for row in rows:
		ip = row.find_element(By.CSS_SELECTOR, "tr > td:nth-child(1)").get_attribute("innerHTML")
		port = row.find_element(By.CSS_SELECTOR, "tr > td:nth-child(2)").get_attribute("innerHTML")
		supports_type = row.find_element(By.CSS_SELECTOR, "tr > td:nth-child(6)").get_attribute("innerHTML")
		async with aiofiles.open(output, 'a+') as f:
			if f"{ip}:{port}" not in await f.readlines() and (types[ptype] == supports_type):
				await f.write(f"{ip}:{port}\n")
		scraped += 1
		os.system("clear | cls")
		print(Panel.fit(f"[blue bold]FreeProxyList[/]\n[blue]Доступно прокси: {len(rows)}[/]\n[green]Scraped: {scraped}[/]"))


async def geonode_scraper(output: str, ptype: str):
	async with aiohttp.ClientSession() as session:
		async with session.get(f'https://proxylist.geonode.com/api/proxy-list?limit=0&page=1&sort_by=lastChecked&sort_type=desc&protocols={ptype}') as response:
			print(Panel.fit(f"[green]Доступно {response.json['total']} прокси[/]"))
			proxies = response.json['data']
			scraped = 0
			for proxy in proxies:
				ip = proxy['ip']
				port = proxy['port']
				async with aiofiles.open(output, 'a+') as f:
					if f"{ip}:{port}" not in await f.readlines():
						await f.write(f"{ip}:{port}\n")
				scraped += 1
				print(Panel.fit(f"[green bold]{scraped}[/]"))
				os.system("clear | cls")
				print(Panel.fit(f"[blue bold]Geonode[/]\n[blue]Доступно прокси: {len(proxies)}[/]\n[green]Scraped: {scraped}[/]"))


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
	hmn_types = ["http", "https", "socks4", "socks5"]
	fplist_types = ["http", "https"]
	geonode_types = ["http", "https", "socks4", "socks5"]
	if ptype in hmn_types and fplist_types and geonode_types:
		print(Panel.fit(f"[green]Скраплю [bold]FreeProxyList[/], [bold]Geonode[/] и [bold]HideMyName[/]"))
		await fplist_scrape(output, ptype)
		await hmn_scrape(output, ptype)
		await geonode_scraper(output, ptype)
		driver.close()
	elif ptype in fplist_types and not hmn_types and geonode_types:
		print(Panel.fit(f"[green]Скраплю [bold]FreeProxyList[/][/]"))
		await hmn_scrape(output, ptype)
	else:
		print(Panel.fit(f"[red]Ошибка произошла какая-то[/]"))


if __name__ == "__main__":
	asyncio.run(menu())
