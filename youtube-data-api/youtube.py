import requests
import json


URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
API_KEY = 'your key'


def print_video_comment(video_id, n=10):
    params = {
        'key': API_KEY,
        'part': 'snippet',
        'videoId': video_id,
        'order': 'relevance',
        'textFormat': 'plaintext',
        'maxResults': n,
    }
    response = requests.get(URL, params=params)
    resource = response.json()

    for comment_info in resource['items']:
        text = comment_info['snippet']['topLevelComment']['snippet']['textDisplay']
        like_cnt = comment_info['snippet']['topLevelComment']['snippet']['likeCount']
        reply_cnt = comment_info['snippet']['totalReplyCount']
        print('{}\nグッド数: {} 返信数: {}\n'.format(text, like_cnt, reply_cnt))


video_id = 'pEfqw4K3MIU'
print_video_comment(video_id, n=5)


def print_video_comment(video_id, n=10):
    params = {
        'key': API_KEY,
        'part': 'snippet',
        'videoId': video_id,
        'order': 'relevance',
        'textFormat': 'plaintext',
        'maxResults': n,
    }
    response = requests.get(URL + 'commentThreads', params=params)
    resource = response.json()

    for comment_info in resource['items']:
        # コメント
        text = comment_info['snippet']['topLevelComment']['snippet']['textDisplay']
        # グッド数
        like_cnt = comment_info['snippet']['topLevelComment']['snippet']['likeCount']
        # 返信数
        reply_cnt = comment_info['snippet']['totalReplyCount']

        print('{}\nグッド数: {} 返信数: {}\n'.format(text, like_cnt, reply_cnt))
