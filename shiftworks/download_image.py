#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shiftworks as sw
import glob
import re


def get_offer_url_list(offer_file):
    # デバック
    print("[Debug] {0}".format(offer_file))
    # 読み込むテキストファイル
    with open(offer_file, 'r') as f:
        url_list = []
        for line in f:
            # 改行を削除
            url = line.strip()
            url_list.append(url)
    return url_list


def get_offer_file_list(search_dir):
    # ファイルを取得
    file_list = glob.glob(search_dir + '/*.txt')
    file_list.remove("./data/2017-09-07/occupation_url_list.txt")
    return file_list


if __name__ == '__main__':
    date = "2017-09-07"
    search_dir = "./data/" + date
    offer_file_list = get_offer_file_list(search_dir)
    for offer_file in offer_file_list:
        industry = re.search(
            r'./data/2017-09-07/offer_(.+)_sjob_.+', offer_file)
        industry = industry.group(1)
        occupation = re.search(
            r'./data/2017-09-07/offer_mjob_.+sjob_(.+).txt', offer_file)
        occupation = "sjob_" + occupation.group(1)
        save_dir = "./image/" + industry + "/" + occupation
        offer_url_list = get_offer_url_list(offer_file)
        for offer_url in offer_url_list:
            img_url_list = sw.get_image_url_list(offer_url)
            if img_url_list != []:
                sw.download_image(img_url_list, save_dir)
