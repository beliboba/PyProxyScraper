from selenium.webdriver.common.by import By

import os
import aiofiles

from rich import print
from rich.panel import Panel


class Info:
	name = "FreeProxyList"
	supported_types = ["http", "https"]


async def scrape(output: str, ptype: str, driver) -> None:
	supported_types = ["http", "https"]
	types = {
		"http": "no",
		"https": "yes"
	}
	scraped = 0
	if ptype not in supported_types:
		print(Panel.fit(f"[red]Неподдерживаемый тип прокси. Поддерживаемые типы: http, https[/]"))
		os.abort()
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
