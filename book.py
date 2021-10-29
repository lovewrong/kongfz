import re

from parsel import Selector
from response import Response


class Book:
    """图书类"""

    def __init__(self, url):
        """初始化"""
        self.url = url
        self.failed = None
        self.title = ''
        self.price = 1
        self.quality = ''
        self.count = 1
        self.cat = ''
        self.info = {}
        self.get_book_info()

    def get_book_info(self):
        # 获取书籍的信息
        sel = Selector(Response(self.url).get().text)
        # 获取书名title、价格price、品相quality
        self.title = sel.css('.title-box h1::attr(itemname)').get()
        self.price = sel.css('.now-price-text-cont::attr(price)').get()
        self.quality = sel.css('.quality-text-cot i::text').get()
        if sel.css('.state-one').get() is None:
            self.count = sel.css('.count-state i::text').get()
        if sel.css('.count-state i::text').get() is None:
            self.count = 0
        a = {
            '书名': self.title,
            '售价': self.price,
            '品相': self.quality,
            '库存': self.count
        }
        self.info.update(a)
        data1 = sel.css('.keywords-define li').getall()
        if data1:
            cat = sel.css('.book-quality-desc a::text').get()
            info = '分类:' + cat + ',' + ','.join(data1)
            info = re.sub(r'<(\S*?)[^>]*>.*?|<.*? />|\s', '', info)
            try:
                d = dict(i.split(":") for i in info.split(","))
                self.info.update(d)
            except:
                self.failed = {'书名': self.title, '网址': self.url}
        data2 = sel.css('.detail-lists li').getall()
        if data2:
            cat = sel.css('.classify-link a::text').get()
            info = '分类:' + cat + ',' + ','.join(data2)
            info = re.sub(r'<(\S*?)[^>]*>.*?|<.*? />|\s', '', info)
            try:
                d = dict(i.split(":") for i in info.split(","))
                self.info.update(d)
            except:
                self.failed = {'书名': self.title, '网址': self.url}
