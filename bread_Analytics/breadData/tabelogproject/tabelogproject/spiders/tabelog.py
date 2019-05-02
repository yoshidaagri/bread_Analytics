from urllib.parse import urlparse, parse_qs
from datetime import datetime
import pytz
import scrapy
import re
#from scrapy.contrib.spiders import 
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
# from tabelogcrawl.items import TabelogcrawlItem
from tabelogproject.items import TabelogprojectItem  # ItemのHeadlineクラスをインポート。

# 1ページ辺り何件取得するか(動作確認時は1とかにする)
LIMIT_GET_PER_PAGE = 20

class TabelogSpider(scrapy.Spider):
    name = 'tabelog'
    allowed_domains = ["tabelog.com"]
    start_urls = (
        #'https://tabelog.com/tokyo/A1319/rstLst/ramen/1/?Srt=D&SrtT=rt&sort_mode=1',
        # 'https://tabelog.com/hokkaido/C1101/rstLst/pan/1/',# 札幌市中央区
        #'https://tabelog.com/hokkaido/C1100/rstLst/SC0101/1/',# 札幌市
        #'https://tabelog.com/hokkaido/rstLst/SC0101/',# 北海道
        #'https://tabelog.com/miyagi/rstLst/SC0101/',# 宮城県
        'https://tabelog.com/niigata/rstLst/SC0101/',# 新潟県
        
        #'https://tabelog.com/miyagi/C4100/rstLst/SC0101/1/',# 仙台市
        #'https://tabelog.com/miyagi/rstLst/SC0101/1',# 宮城県
        #'https://tabelog.com/niigata/A1501/rstLst/SC0101/1/',# 新潟市
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
            # 店ごとに必要な情報をTabelogprojectItemに格納。
            jstnow = pytz.timezone(
                'Asia/Tokyo').localize(datetime.now()).strftime('%Y/%m/%d')
            item = TabelogprojectItem()
            item['date'] = jstnow
            item['name'] = summary.string
            item['score'] = score.string
            href = summary["href"]
            item['link'] = href

            # 店の緯度経度を取得する為、
            # 詳細ページもクローリングしてTabelogprojectItemに格納。
            request = scrapy.Request(
                href, callback=self.parse_child)
            request.meta["item"] = item
            yield request

        # 次ページ。
        soup = BeautifulSoup(response.body, "html.parser")
        # next_page = soup.find('a', class_="page-move__target--next")
        next_page = soup.find('a', class_="c-pagination__arrow c-pagination__arrow--next")
                    
        if next_page:
            href = next_page.get('href')
            yield scrapy.Request(href, callback=self.parse)

    ## 一覧から店情報に移り、情報を取得
    def parse_child(self, response):
        # 店の緯度経度を抽出する。
        # 追加でurl,住所を追加。
        soup = BeautifulSoup(response.body, "html.parser")
        # 緯度経度を取得
        g = soup.find("img", class_="js-map-lazyload")
        longitude, latitude = parse_qs(
            urlparse(g["data-original"]).query)["center"][0].split(",")
        # リンクを取得
        gl = soup.find("p", class_="homepage")
        print("テスト",gl)
        if gl is not None:
            gl2 = gl.select("span")
            print("テスト2",gl2)
            p = re.compile(r"<[^>]*?>")
            #if gl2[0] is not None:
            homepage = p.sub("", gl2[0].string)  # Return hogefugafuga
            #else:
        else:
            homepage = "none"
        
        print("テスト3",homepage)
        # 住所を取得
        
        ga = soup.find("p", class_="rstinfo-table__address")
        print("テスト3.5",ga)
        # print("テスト4",ga)
        if ga is not None:
            p = re.compile(r"<[^>]*?>")
            adress = p.sub("", str(ga))  # Return hogefugafuga
        else:
            adress = "住所なし"    
        print("テスト4",adress)
        item = response.meta["item"]
        item['adress'] = adress
        item['longitude'] = longitude
        item['latitude'] = latitude
        item['homepage'] = homepage
        return item