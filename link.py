from parsel import Selector
from response import Response


class Link:
    def __init__(self, url):
        self.url = url
        self.book_url_list = []
        self.get_book_url_list()

    def get_book_url_list(self):
        sel = Selector(Response(self.url).get().text)
        self.book_url_list = sel.css('.list-content .item-row a::attr(href)').getall()