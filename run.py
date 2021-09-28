import aiohttp
import asyncio
import yarl
import re
import requests

def handle(r):
    # 数据处理
    # 数据有status,text,len,自己写规则过滤
    if r.len > 10:
        print(r.url, r.len)

async def main(url, data={}, cookies={}):
    timeout = aiohttp.ClientTimeout(total=5)   # 休眠5秒
    try:
        async with aiohttp.ClientSession(timeout=timeout, cookies=cookies) as session:
            async with session.post(url, data=data) as res:
                r = RES()
                await r.parse(res)
                handle(r)
                return r
    except:
        pass
    return


class RES():
    # 解析请求体
    def __init__(self):
        self.status = 200
        self.text = ""
        self.len = 0
        self.url = ''

    async def parse(self, res):
        self.text = await res.text()
        self.status = res.status
        self.len = res.content_length
        self.url = res.url



async def parse(URLS):
    tasks = [asyncio.create_task(main(url)) for url in URLS]
    results = await asyncio.gather(*tasks)

if __name__ == '__main__':
    URLs = []  # 填写url队列
    loop = asyncio.get_event_loop()
    task = loop.create_task(parse(URLs))
    loop.run_until_complete(task)

