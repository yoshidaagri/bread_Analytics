import scrapy


# class NewsSpider(scrapy.Spider):
#     name = 'news'# スパイダーの名前
#     # クロール対象とするドメインのリスト
#     allowed_domains = ['news.yahoo.co.jp']
#     # クロールを開始するURLのリスト。１要素のタプルの末尾にはカンマが必要
#     start_urls = [
#         'https://news.yahoo.co.jp/'
#     ]
# 
#     def parse(self, response):
#         print(response.css('ul.topics a::attr("href")').extract())

from yahooproject.items import Headline  # ItemのHeadlineクラスをインポート。

class NewsSpider(scrapy.Spider):
    name = "news"  # Spiderの名前。
    # クロール対象とするドメインのリスト。
    allowed_domains = ["news.yahoo.co.jp"]
    # クロールを開始するURLのリスト。
    start_urls = (
        'https://news.yahoo.co.jp/',
    )

    def parse(self, response):
        """
        トップページのトピックス一覧から個々のトピックスへのリンクを抜き出してたどる。
        """
        print("記事ゲット前")
        print(response.css('ul.toptopics_list a::attr("href")').extract())
        print("リンクはゲット！")
        for url in response.css('ul.toptopics_list a::attr("href")').re(r'/pickup/\d+$'):
            print("記事ゲット開始")
            abs_url = response.urljoin(url)
            yield scrapy.Request(abs_url, self.parse_topics)
            # yield scrapy.Request(response.urljoin(url), self.parse_topics)
        # for url in response.css('ul.toptopics_list a::attr("href")').re(r'/pickup/\d+$'):
            # url を urljoin() で絶対パスに変換
        #    abs_url = response.urljoin(url)

            #yield scrapy.Request(abs_url, self.parse_topics)

    def parse_topics(self, response):
        """
        トピックスのページからタイトルと本文を抜き出す。
        """
        item = Headline()  # Headlineオブジェクトを作成。
        item['title'] = response.css('.newsTitle ::text').extract_first()  # タイトル
        item['body'] = response.css('.hbody').xpath('string()').extract_first()  # 本文
        yield item  # Itemをyieldして、データを抽出する。