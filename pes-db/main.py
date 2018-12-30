import numpy as np
import pandas as pd

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

URL = 'http://pesdb.net/pes2019/'
PLAYER = 'data/player.csv'
PLAYER_DETAIL = 'data/player_detail.csv'


def get_players_id(df, page_num=1):
    if page_num <= 0:
        page_num = 1
    html = urlopen(URL + '?page=' + str(page_num))
    soup = BeautifulSoup(html, 'html.parser')

    id_list = []
    name_list = []
    for row in soup.table.find_all('a', {"href": re.compile('.*?id=.*')}):
        id = re.search(r'./?id=(.+)', row.get('href')).group(1)
        name = row.get_text()

        id_list.append(id)
        name_list.append(name)

    df.id = id_list
    df.name = name_list

    return df


def get_player_detail_info(df, id='7511'):
    html = urlopen(URL + '?id=' + str(id))
    soup = BeautifulSoup(html, 'html.parser')

    player_data = soup.find('table', attrs={'class': 'player'})
    for row in player_data.find_all('tr'):
        print(row)
        print()

    return df


def main():
    # player_df = pd.DataFrame(columns=['id', 'name'])
    # player_df = get_players_id(player_df, page_num=1)
    # player_df.to_csv(PLAYER, index=False)
    # print_df(PLAYER)

    player_detail_df = pd.DataFrame(columns=['id', 'name'])
    player_detail_df = get_player_detail_info(player_detail_df)
    # print_df(PLAYER_DETAIL)


def print_df(path):
    df = pd.read_csv(path)
    print(df.head())


main()
