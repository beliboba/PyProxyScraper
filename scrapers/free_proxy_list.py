from selenium.webdriver.common.by import By

import os
from utils.wtf import wtf

from rich import print
from rich.panel import Panel


class Info:
	name = "FreeProxyList"
	supported_types = ["http", "https"]
	scrape_type = "selenium"


async def scrape(output: str, ptype: str, driver) -> list[str, int]:
	supported_types = ["http", "https"]
	types = {
		"http": "no",
		"https": "yes"
	}
	scraped = 0
	if ptype not in supported_types:
		print(Panel.fit("[red]Неподдерживаемый тип прокси. Поддерживаемые типы: http, https[/]"))
		os.abort()
	driver.get('https://free-proxy-list.net/')
	rows = driver.find_element(By.XPATH, "//*[@id='list']/div/div[2]/div/table/tbody").find_elements(By.TAG_NAME, 'tr')
	print(Panel.fit(f"[blue]Доступно прокси: {len(rows)}[/]"))
	for row in rows:
		ip = row.find_element(By.CSS_SELECTOR, "tr > td:nth-child(1)").get_attribute("innerHTML")
		port = row.find_element(By.CSS_SELECTOR, "tr > td:nth-child(2)").get_attribute("innerHTML")
		supports_type = row.find_element(By.CSS_SELECTOR, "tr > td:nth-child(6)").get_attribute("innerHTML")
		if types[ptype] == supports_type:
			await wtf(output, f"{ip}:{port}")
		scraped += 1
	return [Info.name, scraped]
