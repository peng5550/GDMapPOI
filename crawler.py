import aiohttp
import asyncio
from math import ceil
from openpyxl import Workbook
from datetime import datetime


class PoiCrawler(object):

    def __init__(self):
        self.datas = [["pname", "cityname", "adname", "name", "address", "tel", "location", "location"]]
        self.total_urls = {0}

    async def __get_totals(self, semaphore, link):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with semaphore:
            async with aiohttp.ClientSession(connector=conn) as session:
                async with await session.get(link) as resp:
                    content = await resp.json()
                    totals = int(content.get("count"))
                    page_num = ceil(totals / 20)
                    page_num = page_num if page_num <= 45 else 45
                    new_page_set = {link.replace("page=1", "page={}".format(index)) for index in range(1, page_num + 1)}
                    self.total_urls.update(new_page_set)

    async def __get_content(self, semaphore, link):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with semaphore:
            async with aiohttp.ClientSession(connector=conn) as session:
                async with await session.get(link) as resp:
                    content = await resp.json()
                    print(content)
                    pois = content.get("pois")
                    if pois:
                        return pois
                    return

    async def __crawler(self, semaphore, link):
        content = await self.__get_content(semaphore, link)
        if content:
            for poi_item in content:
                poi_data = [
                    poi_item.get("pname") if poi_item.get("pname") else None,
                    poi_item.get("cityname") if poi_item.get("cityname") else None,
                    poi_item.get("adname") if poi_item.get("adname") else None,
                    poi_item.get("name"),
                    poi_item.get("address") if poi_item.get("address") else None,
                    poi_item.get("tel") if poi_item.get("tel") else None,
                    poi_item.get("location").split(",")[0],
                    poi_item.get("location").split(",")[1]
                ]
                self.datas.append(poi_data)

    def save2excel(self, filePath):
        file_name = f"{filePath}.xlsx"
        wb = Workbook()
        ws = wb.active
        for line in self.datas:
            ws.append(line)
        wb.save(file_name)

    async def taskManager(self, url_list, func):
        tasks = []
        sem = asyncio.Semaphore(5)
        for url in url_list:
            task = asyncio.ensure_future(func(sem, url))
            tasks.append(task)
        await asyncio.gather(*tasks)

    def run(self, search_url_list):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.taskManager(search_url_list, self.__get_totals))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.taskManager(list(self.total_urls)[1:], self.__crawler))



if __name__ == '__main__':
    demo = PoiCrawler()
    search_url_list = [
        'https://restapi.amap.com/v3/place/text?key=8da55afcf541c4479b82fc01062dc6b6&keywords=超市&city=青岛&children=1&offset=20&page=1&extensions=all',
        'https://restapi.amap.com/v3/place/text?key=8da55afcf541c4479b82fc01062dc6b6&keywords=超市&city=上海&children=1&offset=20&page=1&extensions=all',
        'https://restapi.amap.com/v3/place/text?key=8da55afcf541c4479b82fc01062dc6b6&keywords=商场&city=北京&children=1&offset=20&page=1&extensions=all',
        'https://restapi.amap.com/v3/place/text?key=8da55afcf541c4479b82fc01062dc6b6&keywords=商场&city=上海&children=1&offset=20&page=1&extensions=all'
    ]
    area = "青岛"
    keyword = "超市"

    demo.run(search_url_list)
