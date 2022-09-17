import aiofiles
import uvicorn
from sanic import Sanic, text, html
from sanic_jinja2 import SanicJinja2

app = Sanic("main")
jinja = SanicJinja2(app, pkg_name="main", pkg_path="templates")
ptypes = ["http", "https", "socks4", "socks5"]


@app.route("/proxies/<ptype:str>")
async def proxies(request, ptype: str):
	if ptype in ptypes:
		async with aiofiles.open(f'./proxies/{ptype}.txt', 'r') as f:
			return text(await f.read())


@app.route('/')
@jinja.template('index.html')
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


ssl = {
	"cert": "/etc/letsencrypt/live/proxy.italks.su/cert.pem",
	"key": "/etc/letsencrypt/live/proxy.italks.su/key.pem"
}


if __name__ == "__main__":
	uvicorn.run(app, host='0.0.0.0', port=1337, log_level='info', debug=False, ssl_certfile=ssl['cert'], ssl_keyfile=ssl['key'])
