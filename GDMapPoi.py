# coding:utf-8
import threading
from tkinter.ttk import Scrollbar, Combobox
from mttkinter import mtTkinter as tk
from tkinter.messagebox import showinfo, showwarning, showerror
from tkinter import ttk, scrolledtext
from tkinter import filedialog
import aiohttp
import asyncio
from math import ceil
from openpyxl import Workbook


class Application(object):

    def __init__(self):
        self.creatUI()
        self.datas = [["省份", "城市", "区域", "名称", "标签", "地址", "电话", "经度", "纬度"]]
        self.total_urls = {0}
        self.total_num = []

    def creatUI(self):
        self.window = tk.Tk()
        self.window.title("GDMapPoi")
        # 设置窗口大小和位置
        self.window.geometry('960x640+500+50')

        # poi搜索
        # self.oneSearch = tk.Label(self.window, text="Poi搜索", font=self.font)
        # self.oneSearch.place(x=20, y=50)
        # 高德API接口KEY
        self.label_api_key = tk.Label(self.window, text="高德API接口KEY", font=("思源黑体", 11, "bold"))
        self.label_api_key.place(x=20, y=20, width=120, height=25)
        self.entry_api_key = tk.Entry(self.window, font=("思源黑体", 11))
        # self.entry_api_key["values"] = ("b9cb3ad7476d6d6b977340ebdae2f976")
        self.entry_api_key.place(x=20, y=50, width=450, height=25)

        # 数据量
        self.label_totals = tk.Label(self.window, text="数据量", font=("思源黑体", 11, "bold"))
        self.label_totals.place(x=495, y=50, width=50, height=25)
        self.entry_totals = tk.Entry(self.window, font=("思源黑体", 11))
        self.entry_totals.place(x=555, y=50, width=100, height=25)

        # 地 区
        self.label_cities = tk.Label(self.window, text="地 区", font=("思源黑体", 11, "bold"))
        self.label_cities.place(x=740, y=20, width=50, height=25)
        self.entry_cities = scrolledtext.ScrolledText(self.window, font=("思源黑体", 11))
        self.entry_cities.place(x=740, y=50, width=170, height=195)

        # 关键词
        self.label_keywords = tk.Label(self.window, text="关键词", font=("思源黑体", 11, "bold"))
        self.label_keywords.place(x=740, y=245, width=50, height=25)
        self.entry_keywords = scrolledtext.ScrolledText(self.window, font=("思源黑体", 11))
        self.entry_keywords.place(x=740, y=275, width=170, height=195)

        # 查询button
        self.btn_seacch = tk.Button(self.window, text="查询", font=("思源黑体", 11, "bold"),
                                    command=lambda: self.thread_it(self.start_task))
        self.btn_seacch.place(x=740, y=510, width=150, height=30)

        # 导出excel
        self.btn_excel = tk.Button(self.window, text="导出Excel", font=("思源黑体", 11, "bold"),
                                   command=lambda: self.thread_it(self.save2excel))
        self.btn_excel.place(x=740, y=550, width=150, height=30)

        # 数据展示
        title = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.box = ttk.Treeview(self.window, columns=title, show='headings')
        # style = ttk.Style()
        # style.configure("Treeview.Heading", font=("思源黑体", 11, "bold"))
        self.box.place(x=20, y=100, width=700, height=505)
        self.box.column('1', width=50, anchor='center')
        self.box.column('2', width=50, anchor='center')
        self.box.column('3', width=50, anchor='center')
        self.box.column('4', width=150, anchor='center')
        self.box.column('5', width=150, anchor='center')
        self.box.column('6', width=150, anchor='center')
        self.box.column('7', width=100, anchor='center')
        self.box.column('8', width=80, anchor='center')
        self.box.column('9', width=80, anchor='center')
        self.box.heading('1', text='省份')
        self.box.heading('2', text='城市')
        self.box.heading('3', text='区域')
        self.box.heading('4', text='名称')
        self.box.heading('5', text='标签')
        self.box.heading('6', text='地址')
        self.box.heading('7', text='电话')
        self.box.heading('8', text='经度')
        self.box.heading('9', text='纬度')

        self.VScroll1 = Scrollbar(self.box, orient='vertical', command=self.box.yview)
        self.VScroll1.pack(side="right", fill="y")
        self.VScroll2 = Scrollbar(self.box, orient='horizontal', command=self.box.xview)
        self.VScroll2.pack(side="bottom", fill="x")
        # self.VScroll2.place(relx=0.971, rely=0.028, relwidth=0.024, relheight=0.958)
        # self.VScroll1.place(relx=0.971, rely=0.028, relwidth=0.024, relheight=0.958)
        # 给treeview添加配置
        self.box.configure(yscrollcommand=self.VScroll1.set)
        self.box.configure(xscrollcommand=self.VScroll2.set)

    def makeUrls(self):
        keywords = self.entry_keywords.get(0.0, tk.END).strip()
        if not keywords:
            showerror("警告", "请输入关键词!")
            return
        cities = self.entry_cities.get(0.0, tk.END).strip()
        if not cities:
            showerror("警告", "请输入地区!")
            return
        api_key = self.entry_api_key.get().strip()
        if not api_key:
            showerror("警告", "请输入API key!")
            return
        keyword_list = keywords.strip().split("\n")
        city_list = cities.strip().split("\n")

        search_urls = []
        base_url = "https://restapi.amap.com/v3/place/text?key={}&{}&children=1&offset=20&page=1&extensions=all"

        for i in keyword_list:
            for j in city_list:
                search_urls.append(base_url.format(api_key, f"keywords={i}&city={j}"))
        return search_urls, keyword_list[0], city_list[0]

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
                    self.total_num.append(totals)

    async def __get_content(self, semaphore, link):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with semaphore:
            async with aiohttp.ClientSession(connector=conn) as session:
                async with await session.get(link) as resp:
                    content = await resp.json()
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
                    poi_item.get("type") if poi_item.get("type") else None,
                    poi_item.get("address") if poi_item.get("address") else None,
                    poi_item.get("tel") if poi_item.get("tel") else None,
                    poi_item.get("location").split(",")[0],
                    poi_item.get("location").split(",")[1]
                ]
                self.datas.append(poi_data)
                self.box.insert("", "end", values=poi_data)

    def save2excel(self):
        if not self.datas:
            showwarning("警告", "当前不存在任何数据!")
            return
        filePath = filedialog.asksaveasfilename(title="保存文件", filetypes=[("xlsx", ".xlsx")])
        file_name = f"{filePath}.xlsx"
        wb = Workbook()
        ws = wb.active
        for line in self.datas:
            ws.append(line)
        wb.save(file_name)
        showinfo("提示信息", "保存成功！")

    async def taskManager(self, url_list, func):
        tasks = []
        sem = asyncio.Semaphore(5)
        for url in url_list:
            task = asyncio.ensure_future(func(sem, url))
            tasks.append(task)
        await asyncio.gather(*tasks)

    def start(self, search_url_list):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.taskManager(search_url_list, self.__get_totals))

        self.entry_totals.delete(0, tk.END)
        self.entry_totals.insert(tk.END, sum(self.total_num))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.taskManager(list(self.total_urls)[1:], self.__crawler))
        showinfo('提示信息', '查询成功!')

    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    def start_task(self):
        search_urls, keyword, city = self.makeUrls()
        self.start(search_urls)

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    demo = Application()
    demo.run()
