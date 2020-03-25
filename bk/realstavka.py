import bs4
import time
import sqlite3
import datetime
from selenium import webdriver

options = webdriver.ChromeOptions()
#options.add_argument('headless')

driver = webdriver.Chrome(r'C:/Users/admin/PycharmProjects/chromedriver.exe', options=options)
url_xstavka = "https://1xstavka.ru/line/Football/"
miniurl_xstavka = "https://1xstavka.ru/"

conn = sqlite3.connect("books.db")
cursor = conn.cursor()


def get_html_xstavka(url_xstavka):
    driver.get(url_xstavka)
    time.sleep(5)
    html = driver.page_source
    return html


def get_links_xstavka(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    sp = soup.find("ul", class_="liga_menu")
    suuup = sp.find_all("li", class_="")
    for sp in suuup:
        link = sp.find("a", class_="link")
        link = link.get("href")
        yield link


def get_content_xstavka(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    soup = soup.find_all("div", class_="c-events__item c-events__item_col")
    all_games = []
    for s in soup:
        games = []
        datetime = s.find("div", class_="c-events__time-info")
        datetime = datetime.text
        date = datetime[1:7]
        time = datetime[-7:-2]
        if time[-2:] == "45" or time[-2:] == "55" or time[-2:] == "59":
            time = str(int(time[:2]) + 1) + ":00"
            if time[:2] == "24":
                time = "00:00"
                date = str(int(date[:2]) + 1) + ".03"
        games.append(date)
        games.append(time)
        teams = s.find_all("span", class_="c-events__team")
        for team in teams:
            team = team.text
            team = team[:-1]
            if " " in team:
                team = team.split(" ")
                team = team[0]
            games.append(team)
        kefs = s.find_all("a", class_="c-bets__bet c-bets__bet_coef c-bets__bet_sm")
        for kef in kefs:
            kef = kef.text
            kef = kef.strip()
            if len(kef) == 1:
                kef = "1.01"
            games.append(kef)
            if len(games) == 10:
                break
        all_games.append(games)
    return all_games


def prepare(miniurl_xstavka):
    html = get_html_xstavka(url_xstavka)
    for link in get_links_xstavka(html):
        link = miniurl_xstavka + link
        html = get_html_xstavka(link)
        all_games = get_content_xstavka(html)
        game = []
        for i in all_games:
            if len(i) > 9:
                play = (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9])
                game.append(play)
        print(game)
        cursor.executemany("INSERT INTO xstavka VALUES (?,?,?,?,?,?,?,?,?,?)", game)
        conn.commit()

prepare(miniurl_xstavka)
driver.close()