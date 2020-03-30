from selenium import webdriver
import bs4
import time
import sqlite3
import requests
import datetime

conn = sqlite3.connect("books.db")
cursor = conn.cursor()

options = webdriver.ChromeOptions()
#options.add_argument('headless')

driver = webdriver.Chrome(r'C:/Users/admin/PycharmProjects/chromedriver.exe', options=options)
url = "https://tennisi.bet/rt/cgi/!rt_home.CategoryInfo?gameid=5&categoryid=137&more=today&lang=rus"

def get_html(url):
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    return html

def get_content(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    soup = soup.find_all("table")
    all_games = []
    for s in soup:
        strings = s.find_all("tr")
        for string in strings:
            date = string.text
            if "Сегодня" in date:
                date = "20.03"
                game = []
                game.append(date)
            elif date[5:10] == "Марта":
                game = []
                date = date[2:4] + ".03"
                game.append(date)
            else:
                continue
            for s in strings:
                play = s.find_all("td", class_="WO")
                for line in play:
                    line = line.text
                    line = line.strip()
                    if line.isdigit() == True:
                        game = [game[0]]
                    if len(line) > 2:
                        if line[2] == ":":
                            time = line
                            if time[-2:] == "45" or time[-2:] == "55" or time[-2:] == "59":
                                time = str(int(time[:2]) + 1) + ":00"
                                if time[:2] == "24":
                                    time = "00:00"
                                    date = str(int(game[0][:2]) + 1) + ".03"
                                    game = []
                                    game.append(date)
                            game.append(time)
                    if " - " in line:
                        teams = line.split(" - ")
                        for team in teams:
                            if " " in team:
                                team = team.split(" ")
                                adds = ["(%", "(Ауты)", "(Выигранные", "(Офсайды)",
                                        "(Перехваты)", "(Сэйвы)", "(Удары", "(Успешные",
                                        "(Фолы)", "(Угловые)", "(ЖК)"]
                                if team[1] in adds:
                                    break
                                if len(team) > 2:
                                    if team[2] in adds:
                                        break
                                team = team[0]
                            game.append(team)
                    if len(line) > 1:
                        if line[1] == ".":
                            coef = line
                            if len(game) > 3:
                                game.append(coef)
                            if len(game) == 10:
                                if game not in all_games:
                                    all_games.append(game)
                                    break
    return all_games


def prepare():
    html = get_html(url)
    all_games = get_content(html)
    game = []
    for i in all_games:
        play = (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9])
        game.append(play)
        print(play)
    cursor.executemany("INSERT INTO tennisi VALUES (?,?,?,?,?,?,?,?,?,?)", game)
    conn.commit()


if __name__ == "__main__":
    prepare()
    driver.close()