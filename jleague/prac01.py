#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, time, re
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.request import quote
import urllib

#画像をダウンロードする関数
def download_image():
    img_url = "https://iwiz-spo.c.yimg.jp/im_siggXT9ywxWadFtBz2BSuWGfKQ---x215-y280/d/iwiz-sports/soccer/jleague/images/player/1600220.jpg?2017122216"
    save_path = "./image/test.jpg"

    try:
        urllib.request.urlcleanup()
        #写真をダウンロード
        urlretrieve(img_url, save_path)
    except Exception as e:
        #デバック
        print("[Error] {0}".format(e))

download_image()