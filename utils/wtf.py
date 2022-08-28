import aiofiles

"""
Will write desired proxy to output file
"""


async def wtf(output: str, text: str):
	async with aiofiles.open(output, 'a+') as f:
		if text not in await f.readlines():
			await f.write(text + "\n")
