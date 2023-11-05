import asyncio
import os

import httpx
import tqdm
import sqlite3
import bz2
import zipfile
from database_from_csv import database_from_csv


def extractbz2(filepath: str, dstpath: str):
    bz2file = bz2.open(filepath, "rb")
    temp = os.path.join(os.path.dirname(dstpath), "temp.zip")
    with open(temp, "wb") as zip_file:
        zip_file.write(bz2file.read())

    with zipfile.ZipFile(temp, 'r') as zip_ref:
        zip_ref.extractall(dstpath)
    os.remove(temp)


async def dowload_file(url: str, filepath: str):
    temp_bz2 = os.path.join(os.path.dirname(filepath), "temp.bz2")
    with bz2.BZ2File(temp_bz2, "wb") as file:
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", url) as r:
                r.raise_for_status()
                total = int(r.headers.get('content-length', 0))
                tqdm_params = {
                    'desc': url,
                    'total': total,
                    'miniters': 1,
                    'unit': 'it',
                    'unit_scale': True,
                    'unit_divisor': 1024
                }
                with tqdm.tqdm(**tqdm_params) as pb:
                    async for chunk in r.aiter_bytes():
                        pb.update(len(chunk))
                        file.write(chunk)
        file.close()
    extractbz2(temp_bz2, filepath)
    database_from_csv(os.path.join(filepath, "list_of_expired_passports.csv"), "./database")


async def main():
    loop = asyncio.get_running_loop()
    urls = [("https://проверки.гувм.мвд.рф/upload/expired-passports/list_of_expired_passports.csv.bz2",
             "/home/jedmasterson/Desktop")]
    tasks = [loop.create_task(dowload_file(url, filename)) for url, filename in urls]
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
