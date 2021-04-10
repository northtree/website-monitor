import time
import ssl
import asyncio
import aiohttp

from .model import URLStatus
from .kafka import Producer


# https://stackoverflow.com/a/57017274/482899
async def fetch(session: aiohttp.ClientSession, url: str, kafka_producer: Producer) -> URLStatus:
    start = time.time_ns()
    async with session.get(url, ssl=ssl.SSLContext()) as response:
        # TODO: handle request exception
        await response.text()
        end = time.time_ns()
        url_status = URLStatus(url, response.status, start, end)
        kafka_producer.produce(url_status.to_bytes())
        return url_status


async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = []
        kafka_producer = Producer()
        for url in urls:
            tasks.append(fetch(session, url, kafka_producer))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results


if __name__ == '__main__':
    urls = [
        'https://httpbin.org/status/200',
        'https://httpbin.org/status/300',
        'https://httpbin.org/status/400',
        'https://httpbin.org/status/500',
        'https://httpbin.org/delay/1',
        'https://httpbin.org/delay/2',
        # 'https://httpbin.org/delay/10',
        'https://google.com',
    ]
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(fetch_all(urls, loop))
    print(res)
