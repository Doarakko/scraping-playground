import os
import time
import json
from urllib.request import quote, urlopen, urlretrieve

API_KEY = 'dj00aiZpPWdaZHN6QU1VYm84byZzPWNvbnN1bWVyc2VjcmV0Jng9MTA-'
N = 10

# 画像のURLを取得する関数
def get_image_url_list(query):
    endpoint = 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemSearch'
    #画像のサイズ
    image_size = 600
    # オフセット
    # offset =
    #画像サイズを指定しない場合
    # request = '{0}?appid={1}&query={2}&hits={3}'.format(endpoint, API_KEY, quote(query.encode('utf-8')), n)
    request = '{}?appid={}&query={}&hits={}&image_size={}'.format(endpoint, API_KEY, quote(query.encode('utf-8')), N, image_size)
    response = urlopen(request).read()
    resources = json.loads(response.decode('utf-8'))
    # 画像のurlを入れるリストを準備
    url_list = []
    # 画像のURLを抜き取る
    for i in range(0, N):
        #画像サイズを指定しない場合
        #url = resources['ResultSet']['0']['Result'][str(i)]['Image']['Medium']
        url = resources['ResultSet']['0']['Result'][str(i)]['ExImage']['Url']
        url_list.append(url)
    return url_list

#画像をダウンロードする関数
def download_image(img_url_list, query, save_name):
    #画像を保存するディレクトリを指定
    save_dir = './image/' + save_name
    #画像を保存するディレクトリを作成
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    print('Query = \'{}\', n = {}'.format(query, N))
    #初期化
    id = 1
    #ダウンロード成功した回数
    success_cnt = 0
    #ダウンロード失敗した回数
    error_cnt = 0
    # ダウンロード失敗した画像のURLを入れるリストを準備
    error_url_list = []
    for img_url in img_url_list:
        try:
            # 画像を保存するパスを取得
            num = '{0:04d}'.format(id)
            save_path = '{}/{}.jpg'.format(save_dir, save_name + str(num))
            # 写真をダウンロード
            urlretrieve(img_url, save_path)
            success_cnt += 1
            # 1秒スリープ
            time.sleep(1)
            print('[Download] {} {}/{}'.format(query, id, N))
        except Exception as e:
            error_url_list.append(img_url)
            error_cnt += 1
            print('[Error] {} {}/{} {}'.format(query, id, N, img_url))
        id += 1
    print('[Result] {} success:{}/{}'.format(query, success_cnt - error_cnt, success_cnt + error_cnt))
    if N != success_cnt + error_cnt:
        print('[Warning] URL Is Insufficient.')
    # ダウンロード失敗した画像のURL
    for error_url in error_url_list:
        print('[Failed URL] {}'.format(error_url))
    print('')


#テキストファイルから検索するクエリ, 保存する画像のファイル名を取得する関数
def get_query_list(query_list_file_path='./data/query_list.txt'):
    #ロードするテキストファイル
    with open(query_list_file_path) as f:
        #検索するクエリとファイル名を入れるリストを準備
        query_list = []
        for line in f:
            # 改行を削除, カンマで区切る
            query = line.strip().split(',')
            query_list.append(query)
    return query_list

if __name__ == '__main__':
    # テキストファイルから検索するクエリ, 保存するファイル名を取得
    query_list = get_query_list()
    for query in query_list:
        # 画像のURLを取得
        img_url_list = get_image_url_list(query[0])
        # 画像をダウンロード
        download_image(img_url_list, query[0], query[1])
