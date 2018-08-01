from bs4 import BeautifulSoup
from urllib.request import urlopen

LOAD_PATH = './data/top_url.txt'
SAVE_PATH = './data/form_url.txt'

FORM_KEYWORDS = ['問い合わ', '問い合せ', 'contact', 'Contact', 'inquiry', 'Inquiry']
QA_KEYWORDS = ['QA', 'qa', 'aq', 'AQ', 'フォーム', 'form', 'ヘルプ', 'help', ]

def load_file():
    url_list = []
    with open(LOAD_PATH) as f:
        for line in f:
            url = line.strip()
            url_list.append(url)
    print('[Load] {}'.format(LOAD_PATH))
    return url_list

# TOPページのURLから問い合わせフォームのURLを取得
def search_form(top_url):
    try:
        response = urlopen(top_url)
        resources = response.read()
        html = BeautifulSoup(resources, 'html.parser')
        for a_tag in html.find_all('a'):
            li = [a_tag.string, a_tag.get('alt'), a_tag.get('title')]
            for s in li:
                if s is not None and any(key in s for key in FORM_KEYWORDS):
                    form_url = a_tag.get('href')
                    form_url = edit_url(top_url, form_url)
                    print('[Find] {}'.format(form_url))
                    return form_url
        print('Can not find form...'.format())
    except Exception as e:
        print('[Error] {}'.format(e))
    return -1

# URLに 'http' が含まれていない場合, TOPページのURLに連結
def edit_url(top_url, url):
    if url.find('http') == -1:
        if url.find('//'):
            url = top_url + url[1:]
        else:
            url = top_url + url
    return url

if __name__ == '__main__':
    top_url_list = load_file()
    url_cnt = len(top_url_list)
    suc_cnt = 0
    with open(SAVE_PATH, 'w') as f:
        for top_url in top_url_list:
            form_url = search_form(top_url)
            if form_url != -1:
                f.write(form_url + '\n')
                suc_cnt += 1
            else:
                f.write('None\n')
        print('[Save] {}'.format(SAVE_PATH))
    prob = suc_cnt / url_cnt
    print('total: {}\tsuccess: {}\tprob: {:.2}'.format(url_cnt, suc_cnt, prob))
