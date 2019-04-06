#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import datetime
import shiftworks as sw


def get_occupation_url_list(date):
    # 読み込むテキストファイル
    with open('./data/{0}/occupation_url_list.txt'.format(date), 'r') as f:
        url_list = []
        for line in f:
            # 改行を削除
            url = line.strip()
            url_list.append(url)
    return url_list

# テキストファイルを保存するディレクトリを作成・取得する関数


def get_save_dir():
    # テキストファイルを保存するディレクトリを指定
    save_dir = "./data/" + str(datetime.date.today())
    # テキストファイルを保存するディレクトリを作成
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    return save_dir


if __name__ == '__main__':
    # 日付
    # 取得するテキストファイルのディレクトリを指定
    date = "2017-09-13"
    # 職種を取得
    occupation_url_list = get_occupation_url_list(date)
    # 職種ごとの求人を取得
    for occupation_url in occupation_url_list:
        # 初期化
        offer_url_list = []
        # 求人のURLのリスト
        offer_url_list = sw.get_offer_url_list(occupation_url)
        #save_path = "./data/" + get_save_dir + "offer_" + sw.get_industry(occupation_url) + "_" + sw.get_occupation(occupation_url) + ".txt"
        save_path = "{0}/offer_{1}_{2}.txt".format(get_save_dir(), sw.get_industry(
            occupation_url), sw.get_occupation(occupation_url))
        # テキストファイルに保存
        with open(save_path, "w") as f:
            for offer_url in offer_url_list:
                # 書き込み
                f.write(offer_url+'\n')
        # デバック
        print("[Debug] Save \"{0}\"\n".format(save_path))
