from response import Response
from parsel import Selector


class BookList:
    """这是店铺全部商品页面的类"""

    def __init__(self, url):
        """初始化"""
        self.url = url
        self.pager = 1
        self.max_pager = 1
        self.next_url = None
        self.url_list = []
        self.get_list_max_pager()
        self.get_next_list_url()

    def get_list_max_pager(self):
        """全部商品页面的页码最大值"""
        sel = Selector(Response(self.url).get().text)
        self.pager = int(sel.css('.page_num span::text').get())
        max_pager = sel.css('.page_num span::text').getall()[-1]
        # 当商品只有一页时，max_pager为None
        if max_pager:
            self.max_pager = int(max_pager)

    def get_next_list_url(self):
        """获取下一页的链接"""
        sel = Selector(Response(self.url).get().text)
        # 拼接下一页的网址
        if sel.css('.next-btn::attr(href)').get():
            self.next_url = 'https://shop.kongfz.com' + sel.css('.next-btn::attr(href)').get()
