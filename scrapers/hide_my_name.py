from selenium.webdriver.common.by import By

from utils.wtf import wtf

from rich import print
from rich.panel import Panel


class Info:
	name = "HideMyName"
	supported_types = ["http", "https", "socks4", "socks5"]
	scrape_type = "selenium"


async def scrape(output: str, ptype: str, driver) -> list[str, int]:
	driver.get('https://hidemy.name/ru/proxy-list/')
	paginator = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[5]/ul")
	pages = paginator.find_element(By.CSS_SELECTOR, "ul > li:nth-last-child(2)")
	pagecount = int(pages.find_element(By.TAG_NAME, 'a').text)
	scraped = 0
	types = {"http": "h", "https": "s", "socks4": "4", "socks5": "5"}
	print(Panel.fit(f"[blue]Доступно прокси: {pagecount * 64}[/]"))
	for i in range(pagecount):
		driver.get(f'https://hidemy.name/ru/proxy-list/?type={types[ptype]}&start={i*64}#list')
		rows = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[4]/table/tbody")
		for proxyrow in rows.find_elements(By.TAG_NAME, 'tr'):
			ip = proxyrow.find_element(By.CSS_SELECTOR, "tr > td:nth-child(1)").get_attribute("innerHTML")
			port = proxyrow.find_element(By.CSS_SELECTOR, "tr > td:nth-child(2)").get_attribute("innerHTML")
			await wtf(output, f"{ip}:{port}")
			scraped += 1
			return [Info.name, scraped]

