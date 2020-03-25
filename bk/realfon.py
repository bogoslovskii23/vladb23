from selenium import webdriver
import bs4
import time
import sqlite3


options = webdriver.ChromeOptions()
#options.add_argument('headless')

driver = webdriver.Chrome(r'C:/Users/admin/PycharmProjects/chromedriver.exe', options=options)

conn = sqlite3.connect("books.db")
cursor = conn.cursor()

url_fonbet = "https://www.fonbet.ru/#!/bets/football"


def get_html_fonbet(url_fonbet):
    driver.get(url_fonbet)
    time.sleep(10)
    html = driver.page_source
    return html


def get_content_fonbet(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    tags = soup.find_all("tbody", class_="table__body")
    all_games = []
    for t in tags:
        games = t.find_all("tr", class_="table__row")
        for game in games:
            plays = []
            datetime = game.find_all("span")
            for span in datetime:
                span = span.text
                if len(span) > 5:
                    if span[-3] != ":":
                        continue
                    clock = span[-5:]
                    if span[:7] == "Сегодня":
                        date = "20.03"
                    elif span[:6] == "Завтра":
                        date = "21.03"
                    else:
                        date = span[:2] + ".03"
                    if clock[-2:] == "45" or clock[-2:] == "55":
                        clock = str(int(clock[:2]) + 1) + ":00"
                        if clock[:2] == "24":
                            clock = "00:00"
                            date = str(int(date[:2]) + 1) + ".03"
                    plays.append(date)
                    plays.append(clock)
            teams = game.find("h3", "table__match-title-text")
            if teams == None:
                continue
            teams = teams.text
            teams = teams.split(" — ")
            misses = ["нарушения", "офсайды", "угловые", "сейвы", "ауты", "удары", "удаления", "голы"]
            for team in teams:
                if " " in team:
                    team = team.split(" ")
                    team = team[0]
                    if team in misses:
                        break
                plays.append(team)
            kefs = game.find_all("td", class_="table__col _type_btn _type_normal")
            for kf in kefs:
                plays.append(kf.text)
            all_games.append(plays)
    return all_games


def prepare():
    html = get_html_fonbet(url_fonbet)
    all_games = get_content_fonbet(html)
    game = []
    for i in all_games:
        if len(i) > 9:
            play = (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9])
            game.append(play)
            print(play)
    cursor.executemany("INSERT INTO fonbet VALUES (?,?,?,?,?,?,?,?,?,?)", game)
    conn.commit()

prepare()
driver.close()