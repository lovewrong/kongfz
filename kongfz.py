from time import sleep

from pandas import DataFrame as df
from tqdm import tqdm

from book import Book
from booklist import BookList
from link import Link


class Kongfz:
    """这是爬虫的主类"""

    def __init__(self):
        """初始化"""
        self.url = ''
        self.failed_list = []
        self.book_list_url_list = []
        self.book_url_list = []
        self.book_info = []
        self.csv_name = 'default'

    def get_book_list_url_list(self, url):
        book_list = BookList(url)
        self.book_list_url_list.append(book_list.next_url)
        print('\r', f'正在抓取列表页面链接，'
                    f'已经抓取 {len(self.book_list_url_list) - 1} 页，'
                    f'还需抓取 {book_list.max_pager - book_list.pager} 页！', end='')

    def book_list_url_list_append(self):
        while self.book_list_url_list[-1]:
            self.get_book_list_url_list(self.book_list_url_list[-1])
        self.book_list_url_list.remove(None)

    def get_book_url_list(self):
        for url in self.book_list_url_list:
            book_url_list = Link(url)
            self.book_url_list.extend(book_url_list.book_url_list)

    def get_book_info(self):
        for url in tqdm(self.book_url_list):
            book = Book(url)
            if book.failed:
                self.failed_list.append(book.failed)
            if book.info:
                self.book_info.append(book.info)
            else:
                self.failed_list.append({
                    '书名': book.title,
                    '网址': url
                })

    def write(self):
        df(self.book_info).to_csv(f'{self.csv_name}.csv', mode='a', index=False, encoding='utf_8_sig')
        if self.failed_list:
            df(self.failed_list).to_csv('failed.csv', mode='a', index=False, encoding='utf_8_sig')

    def print(self):
        print('**********欢迎使用孔夫子旧书网店铺书籍信息抓取工具**********\n')
        url = input('请输入要抓取的店铺全部商品页面地址：')
        self.url = url
        self.csv_name = input('请输入要保存的文件名：')

    def run(self):
        """主循环"""
        self.print()
        self.book_list_url_list.append(self.url)
        self.get_book_list_url_list(self.url)
        self.book_list_url_list_append()
        self.get_book_url_list()
        print('\n书籍链接抓取完成！正在抓取书籍信息！')
        sleep(0.5)
        self.get_book_info()
        print('书籍信息抓取完成！正在保存到csv文件！')
        self.write()
        print(f'{self.csv_name}.csv文件已保存！')
        if self.failed_list:
            print('failed.csv文件已保存！')
        print(f'本次共成功抓取 {len(self.book_info)} 本书籍，失败 {len(self.failed_list)} 本书籍！')
        input('按任意键退出!')


if __name__ == '__main__':
    k = Kongfz()
    k.run()
