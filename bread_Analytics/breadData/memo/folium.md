# foliumで表示時点で情報をpopupする設定に苦労した話(Google Colab)
## foliumとは
* JavaScriptのLeafletをパースしたライブラリ。
* マップを使って可視化するツール。

## 環境
* google colab

## 実現したいこと
* 収集したパン屋さんの住所から緯度経度を割り出し、地図にプロットする。

## ソース
```pip.py
pip install folium
```

```test.py
import folium

import pandas as pd

chiba_cities = pd.DataFrame({
    'city': ['ハルタ', 'ブルクベーカリー 札幌円山本店', 'DONQ 円山店', 'すぎうらベーカリー 円山店','ペンギンベーカリーカフェ 円山裏参道店'],
    'latitude': [43.057320, 43.056397, 43.055939, 43.056211, 43.054867],
    'longtude': [141.322706, 141.321842, 141.319576, 141.318643,141.321690],
    'population': [1000, 1000, 1000, 1000, 1000]
})

maruyama_map = folium.Map(location=[43.056000, 141.321000], zoom_start=15)

for i, r in chiba_cities.iterrows():
    popup=folium.Popup(r['city'], max_width=1000,show=True)
    folium.Marker(location=[r['latitude'], r['longtude']], popup=popup).add_to(maruyama_map)
maruyama_map
```
## 発生したエラー
```
TypeError: __init__() got an unexpected keyword argument 'show' folium
```
* foliumにshowが無いというエラー。あれ？Githubのソースみてもあるのに。
 
## 何にハマったか？
* Google colabで無意識にpip install foliumすると0.2.1が入る。
* なんと2016年9月バージョン。
* popupクラスのshowは0.6.0に実装。ここです。

## 正解
```pip.py
pip install folium==0.7.0
```

## 教訓
* PyPIのリリースノートはちゃんと読みましょう。


## 参考資料
* PyPI(https://pypi.org/project/folium/)
* Github(https://github.com/python-visualization/folium/issues/831)
  * この#831の2018/03/30レスに「show argument was added in #772,」と書いていて、上記PyPIのリリースノート0.6.0に#772をaddしたと書いている。
