import scrapy
from homepage.items import HomepageItem  # Itemクラスをインポート。
from bs4 import BeautifulSoup
import re
import MySQLdb
from scrapy.utils.project import get_project_settings

class HomepageSpider(scrapy.Spider):
    name = 'headbody'
    # allowed_domains = ['traditionnel.co.jp/']
    # start_urls = (
    #     'http://www.traditionnel.co.jp/',# 札幌市
    # )
    def start_requests(self):
        settings = get_project_settings()
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),  # ホスト
            'db': settings.get('MYSQL_DATABASE', 'breadDB'),  # データベース名
            'user': settings.get('MYSQL_USER', 'devuser'),  # ユーザー名
            'passwd': settings.get('MYSQL_PASSWORD', 'password'),  # パスワード
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),  # 文字コード
        }
        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor()

        sql = 'select homepage from shops where homepage is not null and homepage_crawl_flg = 0 '
        self.c.execute(sql)
        urls = self.c.fetchall()
        print("ホームページ検索結果",urls)
        self.conn.commit()

        for url in urls:
            yield scrapy.Request(
                url[0],
                callback=self.parse
        )

        self.conn.close()

    def parse(self, response):
        # 店のホームページから情報を探索する
        ## BS4を使い、コンテンツをParseする。
        soup = BeautifulSoup(response.body, "html.parser")
        # コメントタグの除去
        # for comment in soup(text=lambda x: isinstance(x, Comment)):
        #     comment.extract()

        # scriptタグの除去
        # for script in soup.find_all('script', src=False):
        #     script.decompose()

        # テキストだけの抽出
        # print(soup.find_all("head"))
        # for text in soup.find_all(text=True):
        #     if text.strip():
        #         print(text)
        item = HomepageItem()
        # print("------------------------------")
        # item['shop_id'] = 1
        item['url'] = response.url
        item['head'] = soup.find("head")
        item['body'] = soup.find("body")
        # item['title'] = "head"

        # request.meta["item"] = item
        # yield request
        yield item
        # print(str(soup.find("head")))
        # print("------------------------------")
        # print(soup.find("head"))
        # print("------------------------------")
        # print(soup.find("body"))
