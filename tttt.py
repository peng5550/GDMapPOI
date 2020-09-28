from tkinter.ttk import Scrollbar
from mttkinter import mtTkinter as tk
import tkinter.font as tf
from tkinter import ttk, scrolledtext


class Application(object):

    def __init__(self):
        self.creatUI()

    def creatUI(self):
        self.window = tk.Tk()
        self.window.title("GDMapPoi")
        # 设置窗口大小和位置
        self.window.geometry('800x650+500+50')
        # 设置字体
        self.font = tf.Font(size=10)

        # poi搜索
        # self.oneSearch = tk.Label(self.window, text="Poi搜索", font=self.font)
        # self.oneSearch.place(x=20, y=50)
        # 地 区
        self.label_totals = tk.LabelFrame(self.window, text="地 区", font=self.font, padx=10, pady=10)
        self.label_totals.place(x=20, y=50)
        self.window_entry_cities = scrolledtext.ScrolledText(self.label_totals, width=20, height=5, wrap=tk.WORD,
                                                             font=tf.Font(size=12))
        self.window_entry_cities.grid()

        # 关键词
        self.label_keywords = tk.LabelFrame(self.window, text="关键词", font=self.font, padx=10, pady=10)
        self.label_keywords.place(x=250, y=50)
        self.window_entry_keywords = scrolledtext.ScrolledText(self.label_keywords, width=20, height=5, wrap=tk.WORD,
                                                               font=tf.Font(size=12))
        self.window_entry_keywords.grid()

        # 高德API接口KEY
        self.label_totals = tk.LabelFrame(self.window, text="高德API接口KEY", font=self.font, padx=10, pady=10)
        self.label_totals.place(x=550, y=80)
        self.window_entry_cities = scrolledtext.ScrolledText(self.label_totals, width=20, height=2, wrap=tk.WORD,
                                                             font=tf.Font(size=11))
        self.window_entry_cities.grid()

        # 数据量
        self.label_totals = tk.LabelFrame(self.window, text="数据量", font=self.font, padx=10, pady=10)
        self.label_totals.place(x=550, y=200)
        self.window_entry_totals = scrolledtext.ScrolledText(self.label_totals, width=20, height=2, wrap=tk.WORD,
                                                             font=tf.Font(size=11))
        self.window_entry_totals.grid()

        # # 查询button
        # self.btn_seacch = tk.Button(self.window, text="查询", font=self.font,
        #                             )
        # self.btn_seacch.place(x=630, y=500, width=150, height=30)
        #
        # # 导出excel
        # self.btn_excel = tk.Button(self.window, text="导出文件", font=self.font,
        #                            )
        # self.btn_excel.place(x=630, y=540, width=150, height=30)
        #
        # 数据展示
        self.label_show_data = tk.LabelFrame(self.window, text="数据展示", font=self.font, padx=10, pady=10)
        self.label_show_data.place(x=20, y=200)
        self.window_showdata = scrolledtext.ScrolledText(self.label_show_data, width=57, height=20, wrap=tk.WORD,
                                                         font=tf.Font(size=11))
        # self.window_showdata.grid()
        # self.scrollbar = tk.Scrollbar(self.window_showdata)
        # self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        title = ['1', '2', '3', '4', '5', '6', '7']
        self.box = ttk.Treeview(self.window_showdata, columns=title, show='headings')

        self.box.place(x=0, y=0, height=20)
        # self.box.grid()
        self.box.column('1', width=50, anchor='center')
        self.box.column('2', width=50, anchor='center')
        self.box.column('3', width=100, anchor='center')
        self.box.column('4', width=100, anchor='center')
        self.box.column('5', width=100, anchor='center')
        self.box.column('6', width=50, anchor='center')
        self.box.column('7', width=50, anchor='center')
        self.box.heading('1', text='省份')
        self.box.heading('2', text='城市')
        self.box.heading('3', text='名称')
        self.box.heading('4', text='地址')
        self.box.heading('5', text='电话')
        self.box.heading('6', text='经度')
        self.box.heading('7', text='纬度')
        self.window_showdata.grid()
        # self.VScroll1 = Scrollbar(self.box, orient='vertical', command=self.box.yview)
        # self.VScroll1.place(relx=0.971, rely=0.028, relwidth=0.024, relheight=0.958)
        # # 给treeview添加配置
        # self.box.configure(yscrollcommand=self.VScroll1.set)

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    demo = Application()
    demo.run()
