Watchaで記録した自分のデータをcsv形式でバックアップ、取り出します。
## 解説記事
[Watchaに記録したデータをスクレイピングでバックアップ-Med Python](https://medpython.blogspot.com/2020/06/watcha-scraping_23.html)

## 使い方

1. 各スクリプトに自分のIDやパスを書き込む

```bash
user_id = ""
email = ""
password_ = ""
```

2. スクレイピング

### 新規・初回

```bash
# 映画
python scripts/watcha_make_csv_new.py -j movie -p log/202006_movie_all.csv
# テレビ
python scripts/watcha_make_csv_new.py -j tv -p log/202006_tv_all.csv
```

### 次回以降

```bash
# yearmonthは、実行時の年月を指定
# 映画
python scripts/watcha_diff.py -j movie -y 202007
# テレビ
python scripts/watcha_diff.py -j tv -y 202007
```

先月分の記録から、差分を取り、追加タイトルがあれば更新してファイルを新規作成。

## できること

1. テレビと映画の両方の記録を取得
2. 自分が記録したタイトルごとに、
- タイトル
- リンク
- 画像のリンク
- 自分の評価
- 自分のレビュー
- ジャンル
- 時間
- 説明
- お気に入り  
を取得

## 必要なライブラリ

```python
import time
from selenium import webdriver
import chromedriver_binary
import bs4
import pandas as pd
import argparse
```

Sleniumはヘッドレスモードで実行。

chrome driverの別途インストールが必要。