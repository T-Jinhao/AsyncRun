import aiohttp
import asyncio
import sys
import yarl
import re
import requests

def handle(r):
    # 数据处理
    # 数据有status,text,len自己写规则过滤
    if r.status == 200:
        print(r.url, r.data)

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
        self.data = ''

    async def parse(self, res, data):
        self.text = await res.text()
        self.status = res.status
        self.len = res.content_length
        self.url = res.url
        self.data = data



async def parse(url, DATA):
    tasks = [asyncio.create_task(main(url, data)) for data in DATA]
    results = await asyncio.gather(*tasks)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        url = sys.argv[1]
        file = sys.argv[2]
        DATA = []
        with open(file, 'r') as F:
            for x in F:
                # 解析请求体
                data = {
                    'key': x
                }
                DATA.append(data.copy())
    else:
        url = ''   # 填写url
        DATA = []  # 填写data队列
    if DATA == []:
        print('usage: python3 run_datas.py url data.txt')
    else:
        loop = asyncio.get_event_loop()
        task = loop.create_task(parse(url, DATA))
        loop.run_until_complete(task)

