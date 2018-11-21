import time
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from util_chatwork import post_messege

TEAM_SCHEDULE_URL = 'https://baseball.yahoo.co.jp/npb/teams/4/schedule'


# 試合日程から試合中のゲームのIDを取得
def search_game_id():
    response = urlopen(TEAM_SCHEDULE_URL)
    resources = response.read()
    html = BeautifulSoup(resources, 'html.parser')
    # print(html)
    if html.find(attrs={'class': 'gameday home active'}) != []:
        for active_cl in html.find(attrs={'class': 'gameday home active'}):
            a_tag = active_cl.find('a')
            i_tag = active_cl.find('i')
            if a_tag is not None and i_tag is not None:
                url = a_tag.get('href')
                game_id = re.search(
                    r'https://baseball.yahoo.co.jp/npb/game/(.+)/', url)
                game_id = game_id.group(1)
                # opponent_team_name = i_tag.string
                return game_id
    elif html.find(attrs={'class': 'gameday away active'}) != []:
        for active_cl in html.find(attrs={'class': 'gameday away active'}):
            a_tag = active_cl.find('a')
            if a_tag is not None and i_tag is not None:
                url = a_tag.get('href')
                game_id = re.search(
                    r'https://baseball.yahoo.co.jp/npb/game/(.+)/', url)
                game_id = game_id.group(1)
                # opponent_team_name = i_tag.string
                return game_id
    return -1


# スコア取得: テキスト速報
def get_score_text(game_id):
    score_board = '[ScoreBoard]\n'
    endpoint = 'https://baseball.yahoo.co.jp/npb/game/'
    url = endpoint + game_id + '/text'
    # print(url)
    response = urlopen(url)
    resources = response.read()
    html = BeautifulSoup(resources, 'html.parser')
    # print(html)
    for tr_tag in html.find_all('tr', attrs={'class': 'yjMS'}):
        for a_tag in tr_tag.find_all('a'):
            if a_tag is not None:
                score_board += a_tag.string + ' '
        td_tag = tr_tag.find('td', attrs={'class': 'sum'})
        if td_tag is not None:
            score_board += td_tag.string + '\n'
    return score_board


# 出場選手名取得
def get_in_player(game_id):
    visitor_players = '[Visitor Player]\n'
    home_players = '[Home Player]\n'
    endpoint = 'https://baseball.yahoo.co.jp/npb/game/'
    url = endpoint + game_id + '/stats'
    # print(url)
    response = urlopen(url)
    resources = response.read()
    html = BeautifulSoup(resources, 'html.parser')
    # print(html)
    for td_tag in html.find_all('td', attrs={'class': 'pn'}):
        for a_tag in td_tag.find_all('a'):
            # print(a_tag.string)
            visitor_players += a_tag.string + '\n'
    return visitor_players, home_players


# テキスト速報取得（得点）
def get_report(game_id):
    all_report = ''
    endpoint = 'https://baseball.yahoo.co.jp/npb/game/'
    url = endpoint + game_id + '/text'
    # print(url)
    response = urlopen(url)
    resources = response.read()
    html = BeautifulSoup(resources, 'html.parser')
    # print(html)得点
    for div_tag in html.find_all('div', attrs={'class': re.compile('^i')}):
        # ~回表/裏
        title_class = div_tag.find('div', attrs={'class': 'title'})
        if title_class is not None:
            title = title_class.find('b')
            # print(title.string)
            all_report += '[' + title.string + ']\n'
        for b_tag in div_tag.find_all('b', attrs={'class': 'red'}):
            # パッター名取得
            a_tag = b_tag.find('a')
            if a_tag is not None:
                # print(a_tag.string)
                all_report += a_tag.string + ':'
            # テキスト取得
            report = re.search(r'<b class=.+><.+</a>(.+)</b>', str(b_tag))
            if report is not None:
                # print(report.group(1))
                all_report += report.group(1) + '\n'
    return all_report


if __name__ == '__main__':
    game_id = search_game_id()
    # print('VS {}'.format(opponent_team_name))
    # print(game_id)
    # print_score_live(game_id)
    # print_score_text(game_id)
    # score_board = get_score_text(game_id)
    # post_messege(score_board)
    # visitor_players, home_players = get_in_player(game_id)
    post_messege(get_report(game_id))
