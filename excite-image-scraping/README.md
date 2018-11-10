# excite-image-scraping
## Overview
「エキサイト 画像検索」から画像のスクレイピングを行います.


## Description
情報解析を目的として「エキサイト 画像検索」から画像のスクレイピングを行います.

### エキサイト・サービス利用規約 （抜粋）
> 第４章　ユーザーの責務
>> 18条（禁止事項）
>>> １．当社は、ユーザーに以下の各号の何れかに該当する事由が生じた場合、ユーザーに対して事前に通知することなく本サービスの利用を停止もしくは登録情報を削除し、又は提供している本サービスを差止め、以後本サービスの利用をお断りすることがあります。なお、停止期間又は一時停止期間も、利用期間に含まれるものとします。
>>>> （２２）他の登録ユーザーのページを閲覧可能とするためのツール等、当社が認めていない非正規のツールもしくは機能を開発し、又はこれを使用する行為。
>>>> （２７）当社が定める一定のデータ容量以上のデータを、本サービスを通じて送信する行為。
>>>> （３６）その他、当社が不適切と判断する行為。

出典：[Excite エキサイト](https://info.excite.co.jp/top/agreement.html)（2018/04/22）

### 著作権法（抜粋）
> 第二章　著作者の権利
>> 第三節　権利の内容
>>> 第五款　著作権の制限
>>> （私的使用のための複製）
>>>> 第四十七条の七　著作物は、電子計算機による情報解析（多数の著作物その他の大量の情報から、当該情報を構成する言語、音、影像その他の要素に係る情報を抽出し、比較、分類その他の統計的な解析を行うことをいう。以下この条において同じ。）を行うことを目的とする場合には、必要と認められる限度において、記録媒体への記録又は翻案（これにより創作した二次的著作物の記録を含む。）を行うことができる。ただし、情報解析を行う者の用に供するために作成されたデータベースの著作物については、この限りでない。
>>>> （電子計算機における著作物の利用に伴う複製）

出典：[電子政府の総合窓口e-Gov イーガブ](http://elaws.e-gov.go.jp/search/elawsSearch/elaws_search/lsg0500/detail?lawId=345AC0000000048&openerCode=1)（2018/04/22）


## Requirement
・mac os 10.13.3  
・anaconda3-5.1.0


## Usage
1. git clone
```
$ git clone https://github.com/Doarakko/scraping
$ cd excite-image-scraping
```
```
./
├── data
│   └── keywords.txt
├── download_image.py
└── image
```

2. keywords.txt に検索するキーワードを入力
```txt:keywords.txt
りんご,apple
オレンジ,orange
```
3. ダウンロードする画像の枚数を入力
```python:download_image.py
N = 60
```
4. スクレイピング
```
$ python download_image.py
```
```
./image/
├── apple
│   ├── apple0001.jpg
│   ├── apple0002.jpg
│   ├── apple0003.jpg
│   ├── apple0004.jpg
│   ├── apple0005.jpg
│   ├── apple0006.jpg
│   ├── apple0007.jpg
│   ├── apple0008.jpg
│   ├── apple0009.jpg
│   ├── apple0010.jpg
│   ├── apple0012.jpg
│   ├── apple0013.jpg
│   ├── apple0014.jpg
│   ├── apple0015.jpg
│   ├── apple0016.jpg
│   ├── apple0017.jpg
│   ├── apple0018.jpg
│   ├── apple0019.jpg
│   └── apple0020.jpg
└── orange
    ├── orange0001.jpg
    ├── orange0002.jpg
    ├── orange0003.jpg
    ├── orange0004.jpg
    ├── orange0005.jpg
    ├── orange0006.jpg
    ├── orange0007.jpg
    ├── orange0008.jpg
    ├── orange0009.jpg
    ├── orange0010.jpg
    ├── orange0011.jpg
    ├── orange0012.jpg
    ├── orange0013.jpg
    ├── orange0014.jpg
    ├── orange0015.jpg
    ├── orange0016.jpg
    ├── orange0017.jpg
    ├── orange0018.jpg
    └── orange0020.jpg
```

## Hint
・[「エキサイト 画像検索」から画像をスクレイピング in Python](https://qiita.com/Doarakko/items/a60437507f3a958b7226)