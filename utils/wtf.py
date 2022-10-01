import aiofiles


async def wtf(output: str, text: str):
	"""Write text to file"""
	async with aiofiles.open(output, 'r') as f:
		contents = await f.readlines()
	async with aiofiles.open(output, 'a+') as f:
		if text + '\n' not in contents:
			await f.write(text + "\n")
