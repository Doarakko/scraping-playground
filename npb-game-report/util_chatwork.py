import requests
from constant import *


def post_messege(message):
    endpoint = 'https://api.chatwork.com/v2'
    url = '{}/rooms/{}/messages'.format(endpoint, ROOM_ID)
    headers = {'X-ChatWorkToken': API_TOKEN}
    params = {'body': message}
    request = requests.post(url, headers=headers, params=params)
