import aiofiles
from sanic import Sanic, text, html

app = Sanic("app")
ptypes = ["http", "https", "socks4", "socks5"]


@app.route("/proxies/<ptype:str>")
async def proxies(request, ptype: str):
	if ptype in ptypes:
		async with aiofiles.open(f'./proxies/{ptype}.txt', 'r') as f:
			return text(await f.read())


@app.route('/')
@app.ext.template('index.html')
async def index(request):
	count = 0
	for ptype in ptypes:
		async with aiofiles.open(f'./proxies/{ptype}.txt', 'r') as f:
			count += len(await f.readlines())
	return {
		'http': app.url_for('proxies', ptype='http'),
		'https': app.url_for('proxies', ptype='https'),
		'socks4': app.url_for('proxies', ptype='socks4'),
		'socks5': app.url_for('proxies', ptype='socks5'),
		'proxycount': count
	}


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=1337)
