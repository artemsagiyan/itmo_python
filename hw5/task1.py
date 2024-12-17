from random import random, randint

import aiofiles
import aiohttp
import asyncio

from datetime import datetime
import os

async def download_random_image(session, path_to_folder):
    print("start")
    randomm = randint(0, 100000000000000)
    url = f'https://api.multiavatar.com/{randomm}.png'
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            path = os.path.join(path_to_folder, str(datetime.now()) + ".png")
            async with aiofiles.open(path, "wb") as f:
                await f.write(await response.content.read())
    except aiohttp.ClientError as e:
        print(f"Ошибка загрузки {url}: {e}")

    print("finished")



async def main():
    dt1 = datetime.now()
    n = 5
    path_to_folder = "./artifacts/task1"
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[download_random_image(session, path_to_folder) for _ in range(n)])

    print(datetime.now() - dt1)


asyncio.run(main())