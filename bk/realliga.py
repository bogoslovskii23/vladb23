import sqlite3
import requests
import bs4
import time


HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
"accept": "*/*"}

conn = sqlite3.connect("books.db")
cursor = conn.cursor()


url_liga = "https://www.ligastavok.ru/bets/my-line/soccer"


def get_html_liga(url_liga, params=None):
    r = requests.get(url_liga, headers=HEADERS, params=params)
    r = r.text
    return r


def get_content_liga(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    soup = soup.find_all("div", class_="events-proposed__wrapper-events-f8fbd6 my-line__events-proposed-28cb52")
    all_games = []
    for i in soup:
        sp = i.find_all("div", class_="bui-event-row-9eed4e bui-event-row_minimize-28fcc8")
        for a in sp:
            teams = []
            date = a.find("div", class_="bui-event-row__date-d4666b")
            date = date.text
            if len(date) == 0:
                break
            date = date[:2] + ".03"
            if date[1] == "-":
                date = "0" + date[0] + ".03"
            time = a.find("span", class_="bui-event-row__time-a6eb59")
            time = time.text
            if time[-2:] == "45" or time[-2:] == "55" or time[-2:] == "59":
                time = str(int(time[:2]) + 1) + ":00"
                if time[:2] == "24":
                    time = "00:00"
                    date = str(int(date[:2]) + 1) + ".03"
            teams.append(date)
            teams.append(time)
            sup = a.find_all("span", class_="bui-commands__command-251fef")
            for t in sup:
                t = t.text
                if " " in t:
                    t = t.split(" ")
                    if t[0] == "НАРУШЕНИЯ" or t[0] == "ОФСАЙДЫ" or t[0] == "УГЛОВЫЕ":
                        break
                    t = t[0]
                teams.append(t)
            if len(teams) < 4:
                break
            cfs = a.find_all("div", class_="bui-outcome-4ce98d")
            for cf in cfs:
                cf = cf.text
                teams.append(cf)
                if teams[-1] == "-":
                    break
            all_games.append(teams)
    return all_games


def prepare():
    html = get_html_liga(url_liga)
    all_games = get_content_liga(html)
    game = []
    for i in all_games:
        if len(i) > 6:
            i[4] = i[4].replace(",", ".")
            i[5] = i[5].replace(",", ".")
            i[6] = i[6].replace(",", ".")
            play = (i[0], i[1], i[2], i[3], i[4], i[5], i[6])
            game.append(play)
            print(play)
    cursor.executemany("INSERT INTO liga VALUES (?,?,?,?,?,?,?)", game)
    conn.commit()

prepare()
