#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, time
import requests
from urllib.request import urlopen
from urllib.request import urlretrieve

API_KEY = 'your key'

#画像を保存するディレクトリを作成・取得する関数
def get_save_dir(save_name):
    #画像を保存するディレクトリを指定
    save_dir = "./image/" + save_name
    #画像を保存するディレクトリを作成
    if not os.path.exists(save_dir): os.makedirs(save_dir)
    return save_dir

#画像を保存するパスを取得する関数
def get_save_path(save_dir, save_name, id):
    num = "{0:04d}".format(id)
    save_path = "{0}/{1}.jpg".format(save_dir, save_name+str(num))
    return save_path

#画像のURLを取得する関数
def get_image_url_list(query, n):
    endpoint = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key='+ API_KEY
    params = {
        'method': 'flickr.photos.search',
        'api_key': API_KEY,
        'text': query,
        'per_page': str(n),
        'format': 'json',
        'nojsoncallback': '1'
    }
    response = requests.get(endpoint, params=params)
    resources = response.json()
    #画像のURLを入れるリストを準備
    url_list = []
    #画像のURLを抜き取る
    for resource in resources['photos']['photo']:
        url = "https://farm{0}.staticflickr.com/{1}/{2}_{3}.jpg".format(str(resource['farm']), resource['server'], resource['id'], resource['secret'])
        url_list.append(url)
    return url_list

#画像をダウンロードする関数
def download_image(img_url_list, query, save_name, n):
    #画像を保存するディレクトリを取得
    save_dir = get_save_dir(save_name)
    #デバック
    print("[Debug] Query = \"{0}\", n = {1}".format(query, n))
    #初期化
    id = 1;
    #ダウンロード成功した回数
    success_cnt = 0
    #ダウンロード失敗した回数
    error_cnt = 0
    #ダウンロード失敗した画像のURLを入れるリストを準備
    error_url_list = []
    for img_url in img_url_list:
        try:
            save_path = get_save_path(save_dir, save_name, id)
            #写真をダウンロード
            urlretrieve(img_url, save_path)
            success_cnt += 1
            #1秒スリープ
            time.sleep(1) 
            #デバック
            print("[Download] {0} {1}/{2}".format(query, id, n))
        except Exception as e:
            error_url_list.append(img_url)
            error_cnt += 1
            #デバック
            print("[Error] {0} {1}/{2} {3}".format(query, id, n, img_url))
        id += 1
    #デバック
    print("[Result] {0} success:{1}/{2}".format(query, success_cnt-error_cnt, success_cnt+error_cnt))
    if n != success_cnt+error_cnt:
        print("[Warning] URL Is Insufficient.")
    #ダウンロード失敗した画像のURL
    for error_url in error_url_list:
        print("[Failed URL] {0}".format(error_url))
    #改行
    print("")
