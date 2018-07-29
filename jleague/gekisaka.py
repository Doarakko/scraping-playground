#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, time, re
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.request import quote

#チーム名とURLを取得する関数
def get_team_list():
    endpoint = 'https://web.gekisaka.jp/club?division_id=73'
    request = endpoint
    response = urlopen(request)
    resources = response.read()
    html = BeautifulSoup(resources, "html.parser")
    
    #チーム名を入れるリストを準備
    team_name_list = []
    #チームのURLを入れるリストを準備
    team_url_list = []
    #選手の詳細ページのURLを抜き取る
    for div_tag in html.find_all("div", attrs={"class":"club_name"}):
        for a_tag in div_tag.find_all("a"):
            url = a_tag.get("href")
            url = 'https:' + url
            #リストに追加
            team_name_list.append(a_tag.string)
            team_url_list.append(url)
    #デバック
    print("[Get] team name and URL")
    return team_name_list, team_url_list

#チーム名とURLをtxt形式で保存する関数
def save_team_list(team_name_list, team_url_list):
    save_dir = "./data/j1/"
    #ファイルを保存するディレクトリを作成
    if not os.path.exists(save_dir): os.makedirs(save_dir)
    #jsonファイルを保存するパス
    save_path = save_dir + "j1_list.txt"

    with open(save_path, 'w') as f:
        for (name, url) in zip(team_name_list, team_url_list):
            f.write(name + "," + url +'\n')
    #デバック
    print("[Save] {0}".format(save_path))

#チーム名とURLをロードする関数
def load_team_list(load_path="./data/j1/j1_list.txt"):
    #チーム名を入れるリストを準備
    team_name_list = []
    #チームのURLを入れるリストを準備
    team_url_list = []

    #読み込むテキストファイル
    with open(load_path, 'r') as f:
        for line in f:
            #改行を削除, カンマで区切る
            query = line.strip().split(',')
            #team_name_list.append(query[0])
            team_url_list.append(query[1])
    return team_url_list
    #return team_name_list, team_url_list

#選手の詳細ページのURLを取得する関数
def get_player_page_url_list(team_url):
    endpoint = team_url
    request = endpoint
    response = urlopen(request)
    resources = response.read()
    html = BeautifulSoup(resources, "html.parser")

    #画像のURLを入れるリストを準備
    url_list = []
    #選手の詳細ページのURLを抜き取る
    for div_tag in html.find_all("div", attrs={"class":"player_result_data"}):
        for a_tag in div_tag.find_all("a"):
            url = a_tag.get("href")
            url = 'https:' + url
            url_list.append(url)
    #デバック
    print("[Get] player page url")
    #画像のURLのリストを返す
    return url_list

#チームのIDを取得する関数
def get_team_id(team_url):
    team_id = re.search(r'https://web.gekisaka.jp/club/detail\?club_id=(.+)', team_url)
    team_id = team_id.group(1)
    return team_id

#選手の詳細ページのURLをtxt形式で保存する関数
def save_player_page_url_list(team_id, player_page_url_list):
    save_dir = "./data/j1/"
    #ファイルを保存するディレクトリを作成
    if not os.path.exists(save_dir): os.makedirs(save_dir)
    #jsonファイルを保存するパス
    save_path = save_dir + "id_" + team_id + ".txt"

    with open(save_path, 'w') as f:
        for player_page_url in player_page_url_list:
            f.write(player_page_url +'\n')
    #デバック
    print("[Save] {0}".format(save_path))

#選手の詳細ページのURLをロードする関数
def load_player_page_url_list(team_id):
    load_path = "./data/j1/id_" + team_id + ".txt" 
    url_list = []

    #読み込むテキストファイル
    with open(load_path, 'r') as f:
        for line in f:
            #改行を削除, カンマで区切る
            query = line.strip()
            url_list.append(query)
    return url_list

#画像のURLを取得する関数
def get_player_image_url(player_page_url):
    request = player_page_url
    response = urlopen(request)
    resources = response.read()
    html = BeautifulSoup(resources, "html.parser")

    #画像のURLを抜き取る
    img_tag = html.find("img", attrs={"class":"geki_image"})
    url = img_tag.get("src")
    url = "https:" + url
    if url != None and url.find(".jpg") != -1:
        return url 
    else:
        return []

#画像の名前を取得する関数
def get_image_name(img_url):
    img_name = re.search(r'https://f.image.geki.jp/data/image/member/.+/.+/.+/(.+).jpg', img_url)
    img_name = img_name.group(1)
    return img_name
    
#画像をダウンロードする関数
def download_image(img_url, team_id):
    #画像の名前を取得
    img_name = get_image_name(img_url)

    save_dir = "./image/id_" + team_id + "/"
    #ファイルを保存するディレクトリを作成
    if not os.path.exists(save_dir): os.makedirs(save_dir)
    save_path = save_dir + img_name + ".jpg"

    try:
        #写真をダウンロード
        urlretrieve(img_url, save_path)
        #1秒スリープ
        time.sleep(2) 
        #デバック
        print("[Download] {0}.jpg".format(img_name))
    except Exception as e:
        #デバック
        print("[Error] {0}".format(img_url))


if __name__ == '__main__':
    #チーム名とURLを取得
    #team_name_list, team_url_list = get_team_list()
    #チーム名とURLをtxt形式で保存
    #save_team_list(team_name_list, team_url_list)
    #チーム名とURLをロード
    team_url_list = load_team_list()
    #team_name_list, team_url_list = load_team_list()
    
    for team_url in team_url_list:
        #選手の詳細ページのURLを取得
        player_page_url_list = get_player_page_url_list(team_url)
        #チームのIDを取得
        team_id = get_team_id(team_url)
        #選手の詳細ページのURLをtxt形式で保存
        #save_player_page_url_list(team_id, player_page_url_list)
        #選手の詳細ページのURLをロード
        player_page_url_list = load_player_page_url_list(team_id)

        for player_page_url in player_page_url_list:
            player_image_url = get_player_image_url(player_page_url)
            download_image(player_image_url, team_id)
            




