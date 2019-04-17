import os
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

async def hold(sec):
    print(f'Running for {sec} seconds')
    print(f'Running in process ID: {os.getpid()}')
    await asyncio.sleep(sec)
    return sec


def async_runer(coro_fn, *args):
    print('entering async_runer')
    sub_loop = asyncio.new_event_loop()
    try:
        coro = coro_fn(*args)
        asyncio.set_event_loop(sub_loop)
        ret = sub_loop.run_until_complete(coro)
        return ret
    finally:
        sub_loop.close()
        print('exit async_runer sub_loop')


async def main(loop):
    print('entering main')
    executor = ProcessPoolExecutor(max_workers=3)
    data = await asyncio.gather(*(loop.run_in_executor(executor, async_runer, hold, sec)
                                  for sec in range(10)))
    print('got result', data)
    print('leaving main')


if __name__ == '__main__':
    _start = time.time()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(main(loop))
    loop.run_until_complete(future)
    print(f"Execution time: { time.time() - _start }")
    loop.close()

