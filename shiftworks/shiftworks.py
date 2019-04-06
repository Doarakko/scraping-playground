# -*- coding: utf-8 -*-
import re
import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve


# URLから業種を取得する関数
def get_industry(occupation_url):
    # 業種
    industry = re.search(r'http://sftworks.jp/list/(.+)/', occupation_url)
    industry = industry.group(1)
    return industry


# URLから職種を取得する関数
def get_occupation(occupation_url):
    # 職種
    occupation = re.search(
        r'http://sftworks.jp/list/mjob_.+/(.+)', occupation_url)
    occupation = occupation.group(1)
    return occupation


# 画像を保存するディレクトリを作成・取得する関数
def get_save_dir(industry, occupation):
    # 画像を保存するディレクトリを指定
    save_dir = "./image/" + industry + "/" + occupation
    # 画像を保存するディレクトリを作成
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    return save_dir


# 保存する画像のファイル名を取得する関数
def get_save_name(img_url):
    save_name = re.search(r'.+photo_id=(.+)&w=400&h=300', img_url)
    save_name = save_name.group(1)
    return save_name


# 画像を保存するパスを取得する関数
def get_save_path(save_dir, save_name):
    save_path = "{0}/{1}.jpg".format(save_dir, save_name)
    return save_path


# 職種ごとのURLを取得する関数
def get_occupation_url_list():
    request = "http://sftworks.jp/select_job"
    response = urlopen(request)
    resources = response.read()
    html = BeautifulSoup(resources, "html.parser")
    print("[Debug] Get Occupation URL.")
    url_list = []
    for list in html.find_all(attrs={"class": "list-alllistitm"}):
        for a_tag in list.find_all("a"):
            url = a_tag.get("href")
            if url is not None and url != "javascript:void(0)":
                url_list.append(url)
    return url_list


# 求人のURLを取得する関数
def get_offer_url_list(occupation_url):
    request = occupation_url
    response = urlopen(request)
    resources = response.read()
    html = BeautifulSoup(resources, "html.parser")

    # 業種
    industry = get_industry(request)
    # 職種
    occupation = get_occupation(request)
    # 画像を保存するディレクトリを作成
    get_save_dir(industry, occupation)

    # デバック
    print("[Debug] Get Offer URL.")
    flag = True
    url_list = []
    for page in range(1, 100):
        if flag:
            request = occupation_url + "?page=" + str(page)
            response = urlopen(request)
            resources = response.read()
            html = BeautifulSoup(resources, "html.parser")
            if html.find_all(attrs={"class": "zero-ttl"}) == []:
                for list in html.find_all(attrs={"class": "workttl"}):
                    for a_tag in list.find_all("a"):
                        url = a_tag.get("href")
                        url_list.append(url)
                        print("[Get Offer URL] {0}".format(url))
            # 求人が0件の場合
            else:
                flag = False
                break
            # 1秒スリープ
            time.sleep(1)
        else:
            break
    return url_list


# 画像のURLを取得する関数
def get_image_url_list(offer_url):
    # 画像のURLを入れるリストを準備
    url_list = []
    try:
        request = offer_url
        response = urlopen(request)
        resources = response.read()
        html = BeautifulSoup(resources, "html.parser")
        # デバック
        print("[Get Image URL] {0}".format(offer_url))
        # 画像のURLを抜き取る
        for list in html.find_all(attrs={"class": "thumb"}):
            for img_tag in list.find_all("img"):
                url = img_tag.get("data-src")
                # 画像のURLのみ入れる
                if url is not None and url.find("//img.sftworks.jp/shift_cu/photoview/") >= 0:
                    url_list.append("http:" + url)
                    # print("[Get Image URL] {0}".format("http:" + url))
    # 求人がすでに削除されていた場合
    except Exception as e:
        print("[Warning] This offer has already been deleted.")
    # 画像のURLのリストを返す
    return url_list


# 画像をダウンロードする関数
def download_image(img_url_list, save_dir):
    if img_url_list != []:
        # 初期化
        # ダウンロード成功した回数
        success_cnt = 0
        # ダウンロード失敗した回数
        error_cnt = 0
        # ダウンロード失敗した画像のurlを入れるリストを準備
        error_url_list = []
        for img_url in img_url_list:
            # 保存する画像のファイル名
            save_name = get_save_name(img_url)
            # 画像を保存するパス
            save_path = get_save_path(save_dir, save_name)
            if not os.path.exists(save_path):
                try:
                    # 写真をダウンロード
                    urlretrieve(img_url, save_path)
                    success_cnt += 1
                    # 1秒スリープ
                    time.sleep(1)
                    print("[Download] {0}".format(save_name))
                except Exception as e:
                    print(e)
                    error_url_list.append(img_url)
                    error_cnt += 1
                    print("[Error] {0} {1}".format(save_name, img_url))
            # ダウンロード済みの画像の場合
            else:
                print("[Warning] This image has already been downloaded.")
        print(
            "[Result] success:{0}/{1}".format(success_cnt, success_cnt+error_cnt))
        # ダウンロード失敗した画像のURL
        for error_url in error_url_list:
            print("[Failed URL] {0}".format(error_url))
        print("")
    else:
        print("[Warning] Image URL does not exist")


'''
job = html.find(attrs={"class":"result-list"}).find("li").string
#業種
industry = re.search(r'(.+)\(', job)
#職種
occupation = re.search(r'\((.+)\)', job)
'''
