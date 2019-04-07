# -*- coding: utf-8 -*-
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import pytz
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from bs4 import BeautifulSoup
from tabelogcrawl.items import TabelogcrawlItem

# 1ページ辺り何件取得するか(動作確認時は1とかにする)
LIMIT_GET_PER_PAGE = 1

class TabelogSpider(scrapy.Spider):
    name = 'tabelog'
# メインクラス
#class TLSpider(CrawlSpider):
#    name = "tlspider"
    allowed_domains = ["tabelog.com"]
    start_urls = (
        'https://tabelog.com/tokyo/A1319/rstLst/ramen/1/?Srt=D&SrtT=rt&sort_mode=1',
    )
    # 20店舗の一覧情報から店名をチョイスする。
    def parse(self, response):
        # 店の情報、店のスコアをリストから抽出。
        ## BS4を使い、コンテンツをParseする。
        soup = BeautifulSoup(response.body, "html.parser")
        summary_list = soup.find_all("a", class_="cpy-rst-name")
        ## スコアは要らない。使用箇所を消す
        score_list = soup.find_all(
            "span", class_="list-rst__rating-val", limit=LIMIT_GET_PER_PAGE)

        for summary, score in zip(summary_list, score_list):
            # 店ごとに必要な情報をTabelogcrawlItemに格納。
            jstnow = pytz.timezone(
                'Asia/Tokyo').localize(datetime.now()).strftime('%Y/%m/%d')
            item = TabelogcrawlItem()
            item['date'] = jstnow
            item['name'] = summary.string
            item['score'] = score.string
            href = summary["href"]
            item['link'] = href

            # 店の緯度経度を取得する為、
            # 詳細ページもクローリングしてTabelogcrawlItemに格納。
            request = scrapy.Request(
                href, callback=self.parse_child)
            request.meta["item"] = item
            yield request

        # 次ページ。
        soup = BeautifulSoup(response.body, "html.parser")
        next_page = soup.find(
            'a', class_="page-move__target--next")
        if next_page:
            href = next_page.get('href')
            yield scrapy.Request(href, callback=self.parse)

    ## 一覧から店情報に移り、情報を取得
    def parse_child(self, response):
        # 店の緯度経度を抽出する。
        # 追加でurl,住所を追加。
        soup = BeautifulSoup(response.body, "html.parser")
        g = soup.find("img", class_="js-map-lazyload")
        longitude, latitude = parse_qs(
            urlparse(g["data-original"]).query)["center"][0].split(",")
        item = response.meta["item"]
        item['longitude'] = longitude
        item['latitude'] = latitude
        return item
