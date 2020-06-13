# usage
# python scripts/watcha_diff.py -j movie -y 202007
# python scripts/watcha_diff.py -j tv -y 202007

import time
from selenium import webdriver
import chromedriver_binary
import bs4
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-y", "--yearmonth")
parser.add_argument("-j", "--janre")
args = parser.parse_args()

user_id = ""
email = ""
password_ = ""
janre = args.janre
yearmonth = args.yearmonth

if janre == "movie":
    # 映画なら
    link_target = "https://watcha.com/ja-JP/users/" + \
        user_id + "/contents/movies/ratings"
else:
    # TVなら
    link_target = "https://watcha.com/ja-JP/users/" + \
        user_id + "/contents/tv_seasons/ratings"

status_img_link_1 = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDMyIDMyIj4KICAgIDxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CiAgICAgICAgPGcgZmlsbD0iI0ZGMkY2RSI+CiAgICAgICAgICAgIDxwYXRoIGQ9Ik01LjgzNCAyNi4xOTFjMCAuNzg4LjY0NiAxLjMzNiAxLjMzOCAxLjMzNi4yNiAwIC41MjctLjA3OC43NjgtLjI1TDE2IDIxLjUzOGw4LjA2IDUuNzRjLjI0Mi4xNzEuNTA4LjI1Ljc2OS4yNS42OTIgMCAxLjMzOC0uNTQ5IDEuMzM4LTEuMzM3VjguNjNhLjUuNSAwIDAgMC0uNS0uNUg2LjMzNGEuNS41IDAgMCAwLS41LjV2MTcuNTYyek0yNi4xNjcgNC4yOTRjMC0uNzM2LS41OTctMS4zMzMtMS4zMzMtMS4zMzNINy4xNjdjLS43MzYgMC0xLjMzMy41OTYtMS4zMzMgMS4zMzNWNi4xM2EuNS41IDAgMCAwIC41LjVoMTkuMzMzYS41LjUgMCAwIDAgLjUtLjVWNC4yOTR6Ii8+CiAgICAgICAgPC9nPgogICAgPC9nPgo8L3N2Zz4K"
status_img_link_2 = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDMyIDMyIj4KICAgIDxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CiAgICAgICAgPGcgZmlsbD0iIzAwQTBGRiI+CiAgICAgICAgICAgIDxwYXRoIGQ9Ik0xNiAxMi43NUEzLjI1NCAzLjI1NCAwIDAgMCAxMi43NSAxNmEuNzUuNzUgMCAwIDEtMS41IDBBNC43NTYgNC43NTYgMCAwIDEgMTYgMTEuMjVhLjc1Ljc1IDAgMCAxIDAgMS41bTAtMi42NjdBNS45MjQgNS45MjQgMCAwIDAgMTAuMDgzIDE2IDUuOTI0IDUuOTI0IDAgMCAwIDE2IDIxLjkxNyA1LjkyNCA1LjkyNCAwIDAgMCAyMS45MTYgMTYgNS45MjQgNS45MjQgMCAwIDAgMTYgMTAuMDgzIi8+CiAgICAgICAgICAgIDxwYXRoIGQ9Ik0xNiAyMy40MTZjLTQuMDkgMC03LjQxNy0zLjMyNy03LjQxNy03LjQxNyAwLTQuMDg5IDMuMzI3LTcuNDE2IDcuNDE3LTcuNDE2UzIzLjQxNiAxMS45MSAyMy40MTYgMTZjMCA0LjA5LTMuMzI3IDcuNDE3LTcuNDE2IDcuNDE3bTE1LjA2LTguNjU0QzI4LjM0IDguOTg0IDIyLjYyMSA1IDE2IDUgOS4zNzggNSAzLjY2MSA4Ljk4NC45NCAxNC43NjJhMi45MzQgMi45MzQgMCAwIDAgMCAyLjQ3NUMzLjY2MSAyMy4wMTUgOS4zNzggMjcgMTYgMjdjNi42MjEgMCAxMi4zNC0zLjk4NCAxNS4wNi05Ljc2MmEyLjkzNCAyLjkzNCAwIDAgMCAwLTIuNDc1Ii8+CiAgICAgICAgPC9nPgogICAgPC9nPgo8L3N2Zz4K"
status_img_link_3 = "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMjRweCIgaGVpZ2h0PSIyNHB4IiB2aWV3Qm94PSIwIDAgMjQgMjQiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogc2tldGNodG9vbCA1MC4yICg1NTA0NykgLSBodHRwOi8vd3d3LmJvaGVtaWFuY29kaW5nLmNvbS9za2V0Y2ggLS0+CiAgICA8dGl0bGU+NjMwMjYxNEEtQzhBMy00MkMwLTlDQzctQTBEQzNDOEM1NTVDPC90aXRsZT4KICAgIDxkZXNjPkNyZWF0ZWQgd2l0aCBza2V0Y2h0b29sLjwvZGVzYz4KICAgIDxkZWZzPjwvZGVmcz4KICAgIDxnIGlkPSJJY29ucy0mYW1wOy1Bc3NldHMiIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIxIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPgogICAgICAgIDxnIGlkPSJJY29uLS8tSWNBZGRXaGl0ZSIgZmlsbD0iI0ZGRkZGRiI+CiAgICAgICAgICAgIDxyZWN0IGlkPSJSZWN0YW5nbGUtMyIgeD0iMTEiIHk9IjQuNSIgd2lkdGg9IjIiIGhlaWdodD0iMTUiIHJ4PSIxIj48L3JlY3Q+CiAgICAgICAgICAgIDxyZWN0IGlkPSJSZWN0YW5nbGUtMy1Db3B5IiB4PSI0LjUiIHk9IjExIiB3aWR0aD0iMTUiIGhlaWdodD0iMiIgcng9IjEiPjwvcmVjdD4KICAgICAgICA8L2c+CiAgICA8L2c+Cjwvc3ZnPg=="


# 先月の年月を作成
def make_last_yearmonth(yearmonth):
    month = str(yearmonth)[4:6]
    year = str(yearmonth)[0:4]
    if month == "01":
        last_yearmonth = str(int(year) - 1) + "12"
        last_yearmonth = int(last_yearmonth)
    else:
        last_yearmonth = int(yearmonth) - 1
    return last_yearmonth


def get_login_after_link(user_id, email, password_, link_):
    url = "https://watcha.com/ja-JP/users/" + user_id
    # headlessモードで
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    login_button = driver.find_element_by_xpath(
        '//*[@id="root"]/div/div[1]/header/nav/div/div/ul/li[3]/button')
    login_button.click()

    # ID/PASSを入力
    id = driver.find_element_by_id("sign_in_email")
    id.send_keys(email)
    password = driver.find_element_by_id("sign_in_password")
    password.send_keys(password_)

    time.sleep(1)

    # ログインボタンをクリック
    login_button = driver.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/div/div/div/section/div/div/form/button')
    login_button.click()

    # ページに遷移
    time.sleep(3)
    driver.get(link_)
    SCROLL_PAUSE_TIME = 1

    # 最下部までスクロール
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # htmlを取得
    time.sleep(5)
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')

    return soup, driver


def get_datail_from_one_page():
    # htmlを取得
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    # 要素を取得
    myreview = soup.find(class_="css-1cplejl-Text el11hez1").text
    detail = soup.find(class_="css-w4pu2t-Detail e1svyhwg15").text
    time_ = soup.find_all(class_="css-1t00yeb-OverviewMeta eokm2782")[-1].text
    # あらすじ
    try:
        synopsis = soup.find(class_="css-oyp1km-Text el11hez1").text
    except AttributeError:
        synopsis = None
    status_link = soup.find(
        class_="contentActionStatusImage css-1l7ppx9-StatusWithImage e1inrba02").span["src"]
    if status_link == status_img_link_1:
        status = "見ている"
    elif status_link == status_img_link_2:
        status = "見たい"
    else:
        status = None

    return myreview, detail, time_, synopsis, status


# 先月のdfを作成
last_ = str(make_last_yearmonth(yearmonth))
csv_path = "log/{}_{}_all.csv".format(last_, janre)
df_last = pd.read_csv(csv_path)

# スクレイピング
soup, driver = get_login_after_link(user_id, email, password_, link_target)
list_movie = []

for i in soup.find_all(class_="css-106b4k6-Self e3fgkal0"):
    title = i.a["title"]
    # 先月のcsvに入っていればスキップ
    if title in list(df_last["タイトル"]):
        # このforを飛ばす
        continue
    else:
        # 下の処理に進む
        print(title)
        pass

    try:
        img_link = i.img["src"]
    except TypeError:
        img_link = None
    link = "https://watcha.com" + i.a["href"]
    rep = i.find(class_="css-172jy0y-ContentRating e3fgkal4").text

    # 各ページに移動
    time.sleep(2)
    driver.get(link)
    time.sleep(5)
    myreview, detail, time_, synopsis, status = get_datail_from_one_page()

    # リストに追加
    list_movie.append([title, link, img_link, rep, myreview,
                       detail, time_, synopsis, status])

driver.close()

# 新しいdfを作成
df_new = pd.DataFrame(
    list_movie,
    columns=["タイトル", "リンク", "画像のリンク", "自分の評価",
             "自分のレビュー", "ジャンル", "時間", "説明", "お気に入り"]
)
df = pd.concat([df_last, df_new])
df.to_csv("log/{}_{}_all.csv".format(str(yearmonth), janre), index=None)
