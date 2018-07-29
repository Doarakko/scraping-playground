#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, time, re, json
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.request import quote

#人物の生年月日を取得する関数
def get_birthday(person_name):
    try:
        endpoint = 'https://ja.wikipedia.org/wiki/'
        request = endpoint + quote(person_name.encode("utf-8"))
        response = urlopen(request)
    except Exception as e:
        #デバック
        print("[Error] name: {0}\tno page".format(person_name))
        return -1
    else:
        resources = response.read()
        html = BeautifulSoup(resources, "html.parser")
        #1秒スリープ
        time.sleep(1)
        #人物のデータを入れるリストを準備
        person_data = []
        #人物の生年月日を抜き取る
        table_tag = html.find("table", class_="infobox")
        if table_tag != None:
            marker = -1
            for a_tag in table_tag.find_all("a"):
                person_data.append(a_tag.string)
            for i in range(0, len(person_data)):
                if person_data[i] != None and person_data[i].find("年") != -1 and person_data[i+1] != None and person_data[i+1].find("月") != -1:
                    marker = i
                    break
            if marker != -1:
                birthday = person_data[marker] + person_data[marker+1]
                #デバック
                print("[Get] name: {0}\tbirthday: {1}".format(person_name, birthday))
                return birthday
            else:
                #デバック
                print("[Error] name: {0}\tno birthday".format(person_name))
                return -1
        else:
            #デバック
            print("[Error] name: {0}\tno page".format(person_name))
            return -1
        
    
if __name__ == '__main__':
    load_path = "./data/actress.txt"
    #load_path = "./data/entertainer.txt"
    #load_path = "./data/idol.txt"

    person_data_list = []
    with open(load_path, 'r') as f:
        for line in f:
            #改行を削除, カンマで区切る
            data = line.strip().split(',')
            person_data_list.append(data)

    save_path = "./data/actress_list.txt"
    #save_path = "./data/entertainer_list.txt"
    #save_path = "./data/idol_list.txt"
    with open(save_path, 'w') as f:
        for person_data in person_data_list:
            #人物の生年月日を取得
            birthday = get_birthday(person_data[0])
            #書き込み
            if birthday != -1:
                #year年month月day日 → year/month/day
                birthday = birthday.replace("年", '/')
                birthday = birthday.replace("月", '/')
                birthday = birthday.replace("日", '')
                f.write(person_data[0] + "," + person_data[1] + "," + birthday + "\n")
            else:
                f.write(person_data[0] + "," + person_data[1] + "," + "null" + "\n")