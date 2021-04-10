import time
import ssl
import asyncio
import aiohttp
import click

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

@click.command()
@click.option('--urls', '-l', default='urls.txt', help='URLs file to monitor')
@click.option('--interval', '-i', default=2, help='Periodic interval in seconds')
@click.option('--count', '-c', default=5, help='Periodic counts in this run')
def main(urls, interval, count):
    with open(urls, 'r') as url_file:
        url_list = url_file.read().splitlines()
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(
            fetch_all(url_list, event_loop, interval, count))

if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
