import MySQLdb

# MySQLサーバーに接続し、コネクションを取得する。
# ユーザー名とパスワードを指定してscrapingデータベースを使用する。
# 接続に使用する文字コードをutf8mb4とする。
# conn = MySQLdb.connect(db='scraping', user='root', passwd='root', charset='utf8mb4')
conn = MySQLdb.connect(host='localhost', port=3306, user='devuser', passwd='password' , db='breadDB', charset='utf8')
c = conn.cursor()  # カーソルを取得する。
# execute()メソッドでSQL文を実行する。
# このスクリプトを何回実行しても同じ結果になるようにするため、
# citiesテーブルが存在する場合は削除する。
c.execute('DROP TABLE IF EXISTS cities')
# citiesテーブルを作成する。
c.execute('''
    CREATE TABLE cities (
        rank integer,
        city text,
        population integer
    )
''')

# execute()メソッドの第2引数にはSQL文のパラメータを指定できる。
# パラメータで置き換える場所（プレースホルダー）は%sで指定する。
c.execute('INSERT INTO cities VALUES (%s, %s, %s)', (1, '上海', 24150000))

# パラメータが辞書の場合、プレースホルダーは %(名前)s で指定する。
c.execute('INSERT INTO cities VALUES (%(rank)s, %(city)s, %(population)s)',
          {'rank': 2, 'city': 'カラチ', 'population': 23500000})

# executemany()メソッドでは複数のパラメータを指定できる。
c.executemany('INSERT INTO cities VALUES (%(rank)s, %(city)s, %(population)s)', [
    {'rank': 3, 'city': '北京', 'population': 21516000},
    {'rank': 4, 'city': '天津', 'population': 14722100},
    {'rank': 5, 'city': 'イスタンブル', 'population': 14160467},
])

conn.commit()  # 変更をコミット（保存）する。

c.execute('SELECT * FROM cities')  # 保存したデータを取得する。
for row in c.fetchall():  # クエリの結果はfetchall()メソッドで取得できる。
    print(row)  # 取得したデータを表示する。

conn.close()  # コネクションを閉じる。