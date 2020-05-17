# my-nintendo-store

Check if [My Nintendo Store](https://store.nintendo.co.jp/) item is in stock.

## Requirements

- Google Chrome
- pipenv

## Usage

1. Download code

```
$ git clone https://github.com/Doarakko/scraping-challenge
$ cd my-nintendo-store
```

2. Set up python environment

```
$ pipenv shell
$ pipenv install
```

3. Download [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
   Check your chrome version and set to `./chromedriver\_\*.zip`.

```
$ unzip chromedriver_mac64.zip
```

4. Set environment variables

```
$ mv .env.example .env
```

Check My Nintendo Store item URL for item id.(`https://store.nintendo.co.jp/item/<item id>.html`)  
`ITEM_ID_LIST` must be comma separated.

```
ITEM_ID_LIST=HAC_Q_AL3PA,HAC_J_ARUUACF1
```

5. Run

```
$ python main.py
「【5/20(水)～5/22(金)お届け】リングフィット アドベンチャー ダウンロード版」は品切れです
「ペーパーマリオ　オリガミキング　ダウンロード版（パッケージ付）」の在庫があります
```

## License

MIT
