# PyProxyScraper
Asynchronous proxy scraper written in python. Supports various proxy lists

## TODO:
1. Proxy checker
2. add more proxy lists
3. replace selenium with pyppeteer

## How to add your proxy lists:
1. Create python file in scrapers/
   2. Create class Info with following variables:
```python
class Info:
   name = ""
   supported_types = ["http", "https", "socks4", "socks5"]

   @staticmethod
   async def geturl(ptype: str):
      return f"https://domain.com/{ptype}"
```
`supported_types` - list of strings
    
`geturl()` - function that returns url for proxy list. Where `ptype` is proxy type

3. Then create function `scrape` wich should return `None`. It must take 2 arguments:`output` and `ptype` both are strings. Output should go in `await wtf(output, proxy)`
4. Done!
