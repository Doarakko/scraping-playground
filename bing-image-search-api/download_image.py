#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import bing_image_search_api as bisa

#テキストファイルから検索するクエリ, 保存する画像のファイル名を取得する関数
def get_query_list(query_list_file_path):
    #読み込むテキストファイル
    with open(query_list_file_path) as f:
        #検索するクエリとファイル名を入れるリストを準備
        query_list = []
        for line in f:
            #改行を削除, カンマで区切る
            query = line.strip().split(',')
            query_list.append(query)
    return query_list

if __name__ == '__main__':
    '''
    #コマンドライン引数を使用する場合
    #テキストファイルのパス
    query_list_file_path = sys.argv[0]
    #ダウンロードする画像の枚数
    n = sys.argv[1]
    '''
    #テキストファイルのパス
    query_list_file_path = "./data/query_list.txt"
    #ダウンロードする画像の枚数
    n = 20
    #テキストファイルから検索するクエリ, 保存するファイル名を取得
    query_list = get_query_list(query_list_file_path)
    for query in query_list:
        #query[0]:検索するクエリ
        #query[1]:保存するファイル名
        save_dir = "./image/" + query[1] + "/"
        if os.path.exists(save_dir):
            image_path_list = glob.glob(save_dir + "*.jpg")
            if len(image_path_list) > 0:
                print("[Skip] {0}".format(query[0]))
                continue

        #画像のURLを取得
        img_url_list = bisa.get_image_url_list(query[0], n)
        #画像をダウンロード
        bisa.download_image(img_url_list, query[0], query[1], n)