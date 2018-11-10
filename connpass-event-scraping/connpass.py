# -*- coding: utf-8 -*-
import sys
import os
import time
import re
import datetime
import requests
from urllib.request import urlopen, urlretrieve, quote
from bs4 import BeautifulSoup


PREFECTURE = '東京都'


def get_today_event():
    cur_date = datetime.datetime.today()
    url = 'https://connpass.com/api/v1/event/'
    params = {
        # yyyymmdd
        'ymd': cur_date.strftime('%Y%m%d')
    }
    response = requests.get(url, params=params)
    resources = response.json()

    for event in resources['events']:
        # hh:mm
        event_end_time = re.search(r'\d\d\d\d-\d\d-\d\dT(\d\d:\d\d):00\+09:00', event['ended_at']).group(1)
        if event['address'][:len(PREFECTURE)] == PREFECTURE and event_end_time > cur_date.strftime('%H:%M') and event['accepted'] < event['limit']:
            event_url = event['event_url']
            is_meal_event(event_url)


def is_meal_event(event_url):
    meal_words = ['懇親会']

    response = urlopen(event_url)
    resources = response.read()
    html = BeautifulSoup(resources, 'html.parser')
    if html.find('懇親会') != 0:
        return True
    else:
        return False

get_today_event()
