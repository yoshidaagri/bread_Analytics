# sqrapyメモ
## 2019/03/19
### 出来たことの復習

## 2019/01/02
### できたこと
* shopテーブルのhomepageを元にshop_homepageテーブルをクロールできた
* https://nori-life.com/setting-url-dynamic-scrapy/
### 今後やること
* bodyが長すぎる場合のカット
* shop_idをparseメソッドに渡すこと
* クロール終了したshop_idを1に更新すること



# sqrapyのインストールでエラーになった際の対処法

## 事象
scrapyをubuntu 18.04にインストールしようとした所、少々エラーが発生したので、
その解決方法を共有することを目的とした投稿です。

pip install scrapy
## 環境
ubuntu 18.04
再インストールしたばかりの状況

## 発生したエラー群
* wheelが無い
* 開発環境（gcc）が無い
* python3-devが無い
* Twistedが無い

## エラーに対する対処
1. wheelが無い　pin install wheel
1. 開発環境（gcc）が無い　sudo apt install build-essential
1. python3-devが無い　sudo apt install python3-dev
1. Twistedが無い　pip install Twisted

## ようやくscrapy
```
$ pip install scrapy
```


```
 error: invalid command 'bdist_wheel'
  
  ----------------------------------------
  Failed building wheel for PyDispatcher
  Running setup.py clean for PyDispatcher
  Running setup.py bdist_wheel for Twisted ... error
  Complete output from command /home/yoshida/pyProject/breadData/bin/python3 -u -c "import setuptools, tokenize;__file__='/tmp/pip-build-imm_816d/Twisted/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" bdist_wheel -d /tmp/tmpsiymix5ypip-wheel- --python-tag cp36:
  usage: -c [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
     or: -c --help [cmd1 cmd2 ...]
     or: -c --help-commands
     or: -c cmd --help
  
  error: invalid command 'bdist_wheel'
  
  ----------------------------------------
  Failed building wheel for Twisted
  Running setup.py clean for Twisted
Failed to build PyDispatcher Twisted
Installing collected packages: cssselect, w3lib, parsel, PyDispatcher, queuelib, pyasn1, pyasn1-modules, service-identity, Twisted, scrapy
  Running setup.py install for PyDispatcher ... done
  Running setup.py install for Twisted ... error
    Complete output from command /home/yoshida/pyProject/breadData/bin/python3 -u -c "import setuptools, tokenize;__file__='/tmp/pip-build-imm_816d/Twisted/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/pip-jlw00lig-record/install-record.txt --single-version-externally-managed --compile --install-headers /home/yoshida/pyProject/breadData/include/site/python3.6/Twisted:


yoshida@yoshida-CFSX4-1:~/github/bread_Analytics/breadData$ # -*- coding: utf-8 -*-
yoshida@yoshida-CFSX4-1:~/github/bread_Analytics/breadData$ source bin/activate(breadData) yoshida@yoshida-CFSX4-1:~/github/bread_Analytics/breadData$ ls
DDL  bin       include  lib64  pyvenv.cfg  tabelog.py      test.py   yahooprojectDML  homepage  lib      memo   share       tabelogproject  test3.py
(breadData) yoshida@yoshida-CFSX4-1:~/github/bread_Analytics/breadData$ cd homepage(breadData) yoshida@yoshida-CFSX4-1:~/github/bread_Analytics/breadData/homepage$ ls
headbody.csv  homepage  scrapy.cfg

1.店の情報を取得する
(breadData) yoshida@yoshida-CFSX4-1:~/github/bread_Analytics/breadData/tabelogproject$ scrapy crawl tabelog -o tabelog.jl


2.HOMEPAGEからURLを取得する
(breadData) yoshida@yoshida-CFSX4-1:~/github/bread_Analytics/breadData/homepage$ scrapy crawl headbody -o headbody.csv

* dockerインストール

sudo curl -L "https://github.com/docker/compose/releases/download/1.12.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose




