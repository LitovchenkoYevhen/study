import asyncio
import random
import urllib.parse
from asyncio import Semaphore
from unittest.mock import Mock

from aiohttp import client, ClientSession
from model_bakery.random_gen import gen_string

servers = [f'test{i}.hell:8100' for i in range(1, 4)]
clients = {}


async def http_request(url, number,  session, semaphore):
    async with semaphore:
        print(f'Starting {number} request')
        async with session.request('GET', url) as resp:
            if resp.status == 200:
                if random.choice([False, True]):
                    raise Exception()
                text = await resp.text()
                print(f'{number} finished')
            return text


def generate_messages():
    for i in range(30):
        path = gen_string(10)
        url = f'http://{random.choice(servers)}/{path}/'
        message = Mock(url=url)
        yield message


async def main():
    tasks = []
    for number, message in enumerate(generate_messages()):
        parsed_url = urllib.parse.urlparse(message.url)
        server = parsed_url.netloc
        session = clients.get(server)
        if not session:
            session = clients[server] = (ClientSession(), Semaphore(10))
        coro = http_request(message.url, number, *session)
        task = asyncio.create_task(coro)
        tasks.append(task)

    results = await asyncio.gather(*[task for task in tasks if not task.done()], return_exceptions=True)
    await close_sessions()


async def close_sessions():

    for session, _ in clients.values():
        await session.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
