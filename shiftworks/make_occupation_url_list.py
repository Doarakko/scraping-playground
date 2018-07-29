#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, datetime
import shiftworks as sw

#テキストファイルを保存するディレクトリを作成・取得する関数
def get_save_dir():
    #テキストファイルを保存するディレクトリを指定
    save_dir = "./data/" + str(datetime.date.today())
    #テキストファイルを保存するディレクトリを作成
    if not os.path.exists(save_dir): os.makedirs(save_dir)
    return save_dir

if __name__ == '__main__':
    #職種
    occupation_url_list = sw.get_occupation_url_list()
    save_path = "{0}/occupation_url_list.txt".format(get_save_dir())
    #テキストファイルに保存
    with open(save_path, "w") as f:
        for occupation_url in occupation_url_list:
            #書き込み
            f.write(occupation_url+'\n')
    #デバック
    print("[Debug] Save {0}".format(save_path))

