#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, time, re, json
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.request import quote

#チーム名とURLを取得する関数
def get_team_list():
    endpoint = 'https://soccer.yahoo.co.jp/jleague/teams/j3'
    request = endpoint
    response = urlopen(request)
    resources = response.read()
    html = BeautifulSoup(resources, "html.parser")
    
    #チーム名を入れるリストを準備
    team_name_list = []
    #チームのURLを入れるリストを準備
    team_url_list = []
    #選手の詳細ページのURLを抜き取る
    for dl_tag in html.find_all("dl", attrs={"class":"team"}):
        #チーム名を取得
        dt_tag = dl_tag.find("dt")
        team_name = dt_tag.string
        for a_tag in dl_tag.find_all("a"):
            url = a_tag.get("href")
            if url.find("players") != -1:
                url = 'https://soccer.yahoo.co.jp' + url
                #リストに追加
                team_name_list.append(team_name)
                team_url_list.append(url)
                break
    #デバック
    print("[Get] team name and URL")
    return team_name_list, team_url_list

#チーム名とURLをtxt形式で保存する関数
def save_team_list(team_name_list, team_url_list):
    save_dir = "./data/j3/"
    #ファイルを保存するディレクトリを作成
    if not os.path.exists(save_dir): os.makedirs(save_dir)
    #jsonファイルを保存するパス
    save_path = save_dir + "j3_list.txt"

    with open(save_path, 'w') as f:
        for (name, url) in zip(team_name_list, team_url_list):
            f.write(name + "," + url +'\n')
    #デバック
    print("[Save] {0}".format(save_path))

#チーム名とURLをロードする関数
def load_team_list(load_path="./data/j3/j3_list.txt"):
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
    div_tag = html.find("div", class_="modBody")
    for tr_tag in div_tag.find_all("tr"):
        for a_tag in tr_tag.find_all("a"):
            url = a_tag.get("href")
            url = 'https://soccer.yahoo.co.jp' + url
            url_list.append(url)
    #デバック
    print("[Get] player page url")
    #画像のURLのリストを返す
    return url_list

#チームのIDを取得する関数
def get_team_id(team_url):
    team_id = re.search(r'https://soccer.yahoo.co.jp/jleague/teams/players/(.+)', team_url)
    team_id = team_id.group(1)
    return team_id

#選手の詳細ページのURLをtxt形式で保存する関数
def save_player_page_url_list(team_id, player_page_url_list):
    save_dir = "./data/j3/"
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
    load_path = "./data/j3/id_" + team_id + ".txt" 
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
    div_tag = html.find("div", attrs={"class":"photo"})
    img_tag = div_tag.find("img")
    url = img_tag.get("src")
    if url != None and url.find(".jpg") != -1:
        return url 
    else:
        return []

#画像の名前を取得する関数
def get_image_name(img_url):
    img_name = re.search(r'https://iwiz-spo.c.yimg.jp/.+/d/iwiz-sports/soccer/jleague/images/player/(.+).jpg?.+', img_url)
    img_name = img_name.group(1)
    return img_name
    
#画像をダウンロードする関数
def download_image(img_url, team_id):
    #画像の名前を取得
    img_name = get_image_name(img_url)

    save_dir = "./image/j3/id_" + team_id + "/"
    #ファイルを保存するディレクトリを作成
    if not os.path.exists(save_dir): os.makedirs(save_dir)
    save_path = save_dir + img_name + ".jpg"

    try:
        #写真をダウンロード
        urlretrieve(img_url, save_path)
        #1秒スリープ
        time.sleep(3) 
        #デバック
        print("[Download] {0}.jpg".format(img_name))
    except Exception as e:
        #デバック
        print("[Error] {0}".format(img_url))

#選手データを取得する関数
def get_player_data(player_page_url):
    request = player_page_url
    response = urlopen(request)
    resources = response.read()
    html = BeautifulSoup(resources, "html.parser")

    player_data = []
    #選手名を抜き取る
    h1_tag = html.find("h1", attrs={"class":"name"}) 
    player_data.append(h1_tag.string)

    #選手データを抜き取る
    for div_tag in html.find_all("div", attrs={"class":"profile"}): 
        for dd_tag in div_tag.find_all("dd"):
            player_data.append(dd_tag.string)
    return player_data

#選手データのリストを辞書に変換する関数
def convert_to_dic(player_data, file_name, team_id):
    #辞書を準備
    player_dic = {}
    key_list = ["name", "birthday", "home"]

    '''
    for (key, player) in zip(key_list, player_data):
        player_dic[key] = player
    '''
    player_dic[key_list[0]] = player_data[0]
    player_dic[key_list[1]] = player_data[4]
    player_dic[key_list[2]] = player_data[5]

    save_dir = "./data/j3/id_" + team_id + "/"
    #ファイルを保存するディレクトリを作成
    if not os.path.exists(save_dir): os.makedirs(save_dir)
    #jsonファイルを保存するパス
    save_path = save_dir + file_name + ".json"
    #辞書をjsonで保存
    with open(save_path, "w") as f: 
        player_json = json.dumps(player_dic)
        json.dump(player_json, f)
    #デバック
    print("[Save] {0}".format(save_path))
    return player_dic



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
        #player_page_url_list = get_player_page_url_list(team_url)
        #チームのIDを取得
        team_id = get_team_id(team_url)

        #選手の詳細ページのURLをtxt形式で保存
        #save_player_page_url_list(team_id, player_page_url_list)
        
        #選手の詳細ページのURLをロード
        player_page_url_list = load_player_page_url_list(team_id)

        for player_page_url in player_page_url_list:
            #画像のURLを取得
            player_image_url = get_player_image_url(player_page_url)
            #画像をダウンロード
            download_image(player_image_url, team_id)
            #選手データを取得
            #player_data = get_player_data(player_page_url)  
            #画像の名前を取得
            #file_name = get_image_name(player_image_url)
            #選手データのリストを辞書に変換
            #player_dic = convert_to_dic(player_data, file_name, team_id)




