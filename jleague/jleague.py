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
    endpoint = 'https://www.jleague.jp'
    request = endpoint + "/club/"
    response = urlopen(request)
    resources = response.read()
    html = BeautifulSoup(resources, "html.parser")
    
    #チーム名を入れるリストを準備
    team_name_list = []
    #チームのURLを入れるリストを準備
    team_url_list = []
    #選手の詳細ページのURLを抜き取る
    for section_tag in html.find_all("section", attrs={"class":"clubTeamArea clearfix"}):
        for a_tag in section_tag.find_all("a"):
            url = a_tag.get("href")
            url = re.search(r'/club/(.+)/day/', url)
            url = url.group(1)
            span_tag = a_tag.find("span")
            #リストに追加
            team_name_list.append(span_tag.string)
            team_url_list.append(url)
    #デバック
    print("[Get] team name and URL")
    return team_name_list, team_url_list

#チーム名とURLをjson形式で保存する関数
def save_team_list(team_name_list, team_url_list):
    save_dir = "./data/"
    #ファイルを保存するディレクトリを作成
    if not os.path.exists(save_dir): os.makedirs(save_dir)
    #jsonファイルを保存するパス
    save_path = save_dir + "team_list.txt"

    with open(save_path, 'w') as f:
        for (name, url) in zip(team_name_list, team_url_list):
            f.write(name + "," + url +'\n')
    #デバック
    print("[Save] {0}".format(save_path))

#チーム名とURLをロードする関数
def load_team_list(load_path="./data/team_list.txt"):
    #チーム名を入れるリストを準備
    #team_name_list = []
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
    endpoint = 'https://www.jleague.jp/club/'

    request = endpoint + team_url + '/day/#player'
    print(request)
    response = urlopen(request)
    resources = response.read()
    html = BeautifulSoup(resources, "html.parser")

    #画像のURLを入れるリストを準備
    url_list = []
    #選手の詳細ページのURLを抜き取る
    section_tag = html.find(attrs={"class":"playerDataTable"})
    

    for tr_tag in section_tag.find_all("tr"):
        url = tr_tag.get("data-href")
        #url_list.append("https://www.softbankhawks.co.jp" + url)
    
    #デバック
    print("[Get] player page url")
    #画像のURLのリストを返す
    return url_list

if __name__ == '__main__':
    #チーム名とURLを取得
    #team_name_list, team_url_list = get_team_list()
    #チーム名とURLをjson形式で保存
    #save_team_list(team_name_list, team_url_list)
    #チーム名とURLをロード
    team_url_list = load_team_list()
    #team_name_list, team_url_list = load_team_list()

    for team_url in team_url_list:
        player_page_url_list = get_player_page_url_list(team_url)
        break




