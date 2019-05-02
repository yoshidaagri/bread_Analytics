import MySQLdb

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class HomepagePipeline(object):
    def process_item(self, item, spider):
        return item

    """
    ItemをMySQLに保存するPipeline。
    """
class ShopHomePagePipeline(object):
    def open_spider(self, spider):
        """
        Spiderの開始時にMySQLサーバーに接続する。
        itemsテーブルが存在しない場合は作成する。
        """

        settings = spider.settings  # settings.pyから設定を読み込む。
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),  # ホスト
            'db': settings.get('MYSQL_DATABASE', 'breadDB'),  # データベース名
            'user': settings.get('MYSQL_USER', 'devuser'),  # ユーザー名
            'passwd': settings.get('MYSQL_PASSWORD', 'password'),  # パスワード
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),  # 文字コード
        }
        self.conn = MySQLdb.connect(**params)  # MySQLサーバーに接続。
        self.c = self.conn.cursor()  # カーソルを取得。
        # itemsテーブルが存在しない場合は作成。
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS shop_homepage (
                    shop_id INT NOT NULL AUTO_INCREMENT,
                    url varchar(512) NOT NULL,
                    head text,
                    body text,
                    PRIMARY KEY(shop_id,url)
            )
        ''')
        self.conn.commit()  # 変更をコミット。
    def close_spider(self, spider):
        """
        Spiderの終了時にMySQLサーバーへの接続を切断する。
        """

        self.conn.close()
    def process_item(self, item, spider):
        """
        Itemをitemsテーブルに挿入する。
        """
        # sql = "INSERT INTO shop_homepage(shop_id,url,head,body) VALUES (%s, %s, %s, %s)"
        sql = "INSERT INTO shop_homepage(url,head,body) VALUES (%s, LEFT(%s,65534), LEFT(%s,65534))"
        # sql = "INSERT INTO shops(name,score,tabe_url) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        curs = self.conn.cursor()
        # curs.execute(sql, (item['shop_id'], item['url'], item['head'], item['body']))
        curs.execute(sql, (item['url'], item['head'], item['body']))
        self.conn.commit()
        # self.c.execute('INSERT INTO shops (name) VALUES (%(title)s)', dict(item))
        # self.conn.commit()  # 変更をコミット。
        return item
