# PyProxyScraper
Asynchronous proxy scraper written in python. Supports various proxy lists

TODO:
1. Proxy checker
2. add more proxy lists
3. replace selenium with pyppeteer

How to add your proxy lists:
1. Create python file in scrapers/
2. Create class Info with following variables:
    ```python
    class Info:
        name = ""
        supported_types = ["http", "https", "socks4", "socks5"]
        scrape_type = "aiohttp"
    ```
    `supported_types` - list of strings
    
    `scrape_type `- can be `aiohttp` or `selenium`

3. Then create function `scrape` wich should return `None`. It must take 2 arguments:`output` and `ptype` both are strings. If `scrape_type` is `selenium` it also should take `driver` argument (`WebDriver`)
4. Done!