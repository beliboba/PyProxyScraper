from selenium.webdriver.common.by import By

import os
import aiofiles

from rich import print
from rich.panel import Panel


class Info:
	name = "HideMyName"
	supported_types = ["http", "https", "socks4", "socks5"]


async def scrape(output: str, ptype: str, driver) -> None:
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

