from selenium import webdriver
import bs4
import time
import sqlite3
import json


options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(r'C:/Users/admin/PycharmProjects/chromedriver.exe', options=options)


conn = sqlite3.connect("books.db")
cursor = conn.cursor()


url = "https://ad.betcity.ru/d/off/events?rev=6&ver=100&csn=ooca9s"


def get_html(url):
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    return html


def get_content(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    dict = json.loads(soup.find("body").text)
    b = dict["reply"]["sports"]["1"]["chmps"]
    b = b.keys()
    all_games = []
    for key in b:
        h = dict["reply"]["sports"]["1"]["chmps"][key]["evts"]
        p = h.keys()
        for cluc in p:
            game = []
            a = dict["reply"]["sports"]["1"]["chmps"][key]["evts"][cluc]
            datetime = dict["reply"]["sports"]["1"]["chmps"][key]["evts"][cluc]["date_ev_str"]
            date = datetime[:-6]
            date = date[-2:] + "." + date[5:7]
            time = datetime[-5:]
            if time[-2:] == "45" or time[-2:] == "55" or time[-2:] == "59":
                time = str(int(time[:2]) + 1) + ":00"
                if time[:2] == "24":
                    time = "00:00"
                    date = str(int(date[:2]) + 1) + ".03"
            game.append(date)
            game.append(time)
            team1 = dict["reply"]["sports"]["1"]["chmps"][key]["evts"][cluc]["name_ht"]
            if " " in team1:
                team1 = team1.split(" ")
                team1 = team1[0]
            game.append(team1)
            t = a.keys()
            if "name_at" not in t:
                continue
            team2 = dict["reply"]["sports"]["1"]["chmps"][key]["evts"][cluc]["name_at"]
            if " " in team2:
                team2 = team2.split(" ")
                team2 = team2[0]
            game.append(team2)
            c = dict["reply"]["sports"]["1"]["chmps"][key]["evts"][cluc]["main"]
            c = c.keys()
            if "69" not in c:
                continue
            win1 = dict["reply"]["sports"]["1"]["chmps"][key]["evts"][cluc]["main"]["69"]["data"][cluc]["blocks"]["Wm"]["P1"]["kf"]
            game.append(win1)
            c = dict["reply"]["sports"]["1"]["chmps"][key]["evts"][cluc]["main"]["69"]["data"][cluc]["blocks"]["Wm"]
            c = c.keys()
            if "X" not in c:
                continue
            draw = dict["reply"]["sports"]["1"]["chmps"][key]["evts"][cluc]["main"]["69"]["data"][cluc]["blocks"]["Wm"]["X"]["kf"]
            game.append(draw)
            win2 = dict["reply"]["sports"]["1"]["chmps"][key]["evts"][cluc]["main"]["69"]["data"][cluc]["blocks"]["Wm"]["P2"]["kf"]
            game.append(win2)
            v = dict["reply"]["sports"]["1"]["chmps"][key]["evts"][cluc]["main"]["70"]["data"][cluc]["blocks"]["WXm"]
            v = v.keys()
            if "1X" in v:
                wd1 = dict["reply"]["sports"]["1"]["chmps"][key]["evts"][cluc]["main"]["70"]["data"][cluc]["blocks"]["WXm"]["1X"]["kf"]
                game.append(wd1)
                ww12 = dict["reply"]["sports"]["1"]["chmps"][key]["evts"][cluc]["main"]["70"]["data"][cluc]["blocks"]["WXm"]["12"]["kf"]
                game.append(ww12)
                wd2 = dict["reply"]["sports"]["1"]["chmps"][key]["evts"][cluc]["main"]["70"]["data"][cluc]["blocks"]["WXm"]["X2"]["kf"]
                game.append(wd2)
            all_games.append(game)
    return  all_games


def prepare():
    html = get_html(url)
    all_games = get_content(html)
    game1 = []
    game2 = []
    for i in all_games:
        if i[2] == "УГЛ":
            continue
        if len(i) == 10:
            play = (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9])
            game1.append(play)
            print(play)
        if len(i) == 7:
            match  = (i[0], i[1], i[2], i[3], i[4], i[5], i[6])
            game2.append(match)
    cursor.executemany("INSERT INTO city VALUES (?,?,?,?,?,?,?,?,?,?)", game1)
    conn.commit()
    cursor.executemany("INSERT INTO minicity VALUES (?,?,?,?,?,?,?)", game2)
    conn.commit()


if __name__ == "__main__":
    prepare()

