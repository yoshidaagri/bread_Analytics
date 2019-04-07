import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from yahooproject.items import Headline  # ItemのHeadlineクラスをインポート。

class NewsSpider(scrapy.Spider):
    name = "news_crawl"  # Spiderの名前。
    # クロール対象とするドメインのリスト。
    allowed_domains = ["news.yahoo.co.jp"]
    # クロールを開始するURLのリスト。
    start_urls = (
        'https://news.yahoo.co.jp/',
    )
    # リンクをたどるためのルールのリスト。
    rules = (
        # トピックスのページへのリンクをたどり、レスポンスをparse_topics()メソッドで処理する。
        Rule(LinkExtractor(allow=r'/pickup/\d+$'), callback='parse_topics'),
    )

    def parse_topics(self, response):
        """
        トピックスのページからタイトルと本文を抜き出す。
        """
        item = Headline()
        item['title'] = response.css('.newsTitle ::text').extract_first()
        item['body'] = response.css('.hbody').xpath('string()').extract_first()
        yield item