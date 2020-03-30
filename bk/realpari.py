from selenium import webdriver
import bs4
import time
import sqlite3


HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
"accept": "*/*"}

options = webdriver.ChromeOptions()
#options.add_argument('headless')

driver = webdriver.Chrome(r'C:/Users/admin/PycharmProjects/chromedriver.exe', options=options)

url_pari = "https://www.parimatch.ru/prematch/all/1%7CF"

conn = sqlite3.connect("books.db")
cursor = conn.cursor()



def get_html_pari(url_pari):
    driver.get(url_pari)
    time.sleep(100)
    html = driver.page_source
    return html


def get_content_pari(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    matches = soup.find_all("prematch-block", class_="prematch-block")
    all_games = []
    for match in matches:
        games = []
        datetime = match.find("div", class_="live-block-time")
        if datetime == None:
            break
        datetime = datetime.text
        date = datetime[1:6]
        time = datetime[-6:-1]
        if time[-2:] == "45" or time[-2:] == "55" or time[-2:] == "59":
            time = str(int(time[:2]) + 1) + ":00"
            if time[:2] == "24":
                time = "00:00"
                date = str(int(date[:2]) + 1) + ".03"
        games.append(date)
        games.append(time)
        teams = match.find_all("span", class_="competitor-name")
        for team in teams:
            team = team.text
            if " " in team:
                team = team.split(" ")
                misses = ["нарушения", "офсайды", "угловые", "сейвы", "ауты", "удары", "удаления", "голы"]
                if team[0] in misses:
                    break
                team = team[0]
            games.append(team)
        kefs = match.find("div", class_="main-markets-group-outcome outcome")
        kefs = kefs.find_all("div", class_="outcome")
        for kef in kefs:
            kef = kef.text
            games.append(kef)
        all_games.append(games)
    return all_games

def prepare():
    html = get_html_pari(url_pari)
    all_games = get_content_pari(html)
    game = []
    for i in all_games:
        if len(i) > 6:
            if i[4] == " ":
                continue
            play = (i[0], i[1], i[2], i[3], i[4], i[5], i[6])
            game.append(play)
            print(play)
    cursor.executemany("INSERT INTO pari VALUES (?,?,?,?,?,?,?)", game)
    conn.commit()


if __name__ == "__main__":
    prepare()
    driver.close()