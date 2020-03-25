from selenium import webdriver
import bs4
from selenium.webdriver.support.ui import WebDriverWait
import time
import sqlite3


options_winline = webdriver.ChromeOptions()
#options_winline.add_argument('headless')

driver_winline = webdriver.Chrome(r'C:/Users/admin/PycharmProjects/chromedriver.exe', options=options_winline)
url_winline = "https://winline.ru/stavki/sport/futbol/"

#conn = sqlite3.connect("books.db")
#cursor = conn.cursor()


def get_html_winline(url_winline):
    for i in range(3):
        driver_winline.get(url_winline)
        time.sleep(10)
        html = driver_winline.page_source
        yield html


def get_content_winline(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    soup = soup.find_all("div", class_="ng-scope")
    all_games = []
    n = 1
    for i in soup:
        sp = i.find_all("div", class_="table ng-scope")
        for s in sp:
            x = s.find("div", class_="statistic")

            print(x.text)

            games = []
            """date = s.find("div", class_="statistic__date ng-binding ng-scope")
            date = date.text
            date = date.replace("/", ".")
            games.append(date)
            time = s.find("a", class_="statistic__time ng-binding ng-scope")
            time = time.text
            games.append(time)"""
            teams = s.find("div", class_="statistic__wrapper")
            if teams == None:
                continue
            teams = teams.find_all("span", class_="ng-binding")
            for team in teams:
                games.append(team.text)
            games = games[0:2]
            coefs = s.find_all("div", class_="coefficient__td table__td ng-binding")
            if coefs != []:
                for coef in coefs:
                    games.append(coef.text)
                all_games.append(games)
            else:
                continue
    return all_games

def prepare():
    htmls = get_html_winline(url_winline)
    for html in htmls:
        all_games = get_content_winline(html)
        game = []
        for i in all_games:
            if len(i) > 6:
                play = (i[0], i[1], i[2], i[3], i[4], i[5], i[6])
                game.append(play)
                #print(play)
        #cursor.executemany("INSERT INTO winline VALUES (?,?,?,?,?,?,?)", game)
        #conn.commit()


prepare()