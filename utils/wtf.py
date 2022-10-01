import aiofiles


async def wtf(output: str, text: str):
	"""Write text to file"""
	async with aiofiles.open(output, 'a+') as f:
		if text not in await f.readlines():
			await f.write(text + "\n")
