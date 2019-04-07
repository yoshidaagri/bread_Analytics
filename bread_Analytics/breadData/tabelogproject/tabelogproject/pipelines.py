import MySQLdb

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TabelogprojectPipeline(object):
    def process_item(self, item, spider):
        return item

class MySQLPipeline(object):
    """
    ItemをMySQLに保存するPipeline。
    """

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
        # self.c.execute('DROP TABLE IF EXISTS shops')
        # itemsテーブルが存在しない場合は作成。
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS shops (
                    shop_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                    city_id INT,
                    name varchar(255),
                    date date,
                    score decimal(3,2),
                    tabe_url varchar(512),
                    longitude decimal(17,14),
                    latitude decimal(17,14),
                    homepage varchar(512),
                    adress varchar(512),
                    homepage_crawl_flg int DEFAULT 0
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
        sql = "INSERT INTO shops(name,score,tabe_url,longitude,latitude,homepage,adress) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        # sql = "INSERT INTO shops(name,score,tabe_url) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        curs = self.conn.cursor()
        curs.execute(sql, (item['name'], item['score'], item['link'], item['longitude'], item['latitude'], item['homepage'], item['adress']))
        self.conn.commit()
        # self.c.execute('INSERT INTO shops (name) VALUES (%(title)s)', dict(item))
        # self.conn.commit()  # 変更をコミット。
        return item