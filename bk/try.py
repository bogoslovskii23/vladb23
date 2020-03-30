
















import sqlite3

conn = sqlite3.connect("books.db")
cursor = conn.cursor()

parimatch = "SELECT * FROM pari"
xstavka = "SELECT * FROM xstavka"
fonbet = "SELECT * FROM fonbet"
ligastavok = "SELECT * FROM liga"
tennisi = "SELECT * FROM tennisi"
betcity = "SELECT * FROM city"
minicity = "SELECT * FROM minicity"

def get_games(bk):
    cursor.execute(bk)
    games = cursor.fetchall()
    return games

parimatch = get_games(parimatch)
fonbet = get_games(fonbet)
xstavka = get_games(xstavka)
ligastavok = get_games(ligastavok)
tennisi = get_games(tennisi)
betcity = get_games(betcity)
minicity = get_games(minicity)

all_games = [parimatch, fonbet, xstavka, ligastavok, tennisi, betcity, minicity]

def sravnenie(bk1, bk2):
    matches = []
    for game in bk1:
        if bk1 == bk2:
            break
        for play in bk2:
            if len(play) == 10 and play[7] != "-":
                if game[0][:2] == play[0][:2] and game[1][:5] == play[1][:5]:
                    if game[2] == play[2] or game[3] == play[3]:
                        match = [game[0], game[1], game[2], play[2], play[3], game[3]]
                        n = 4
                        m = 9
                        while n < 7:
                            kef = 1 / float(game[n]) + 1 / float(play[m])
                            if kef < 1:
                                match.append(game[n])
                                match.append(play[m])
                                match.append((n))
                            n += 1
                            m -= 1
                        if len(match) > 6:
                            matches.append(match)
    return matches

for games in all_games:
    for plays in all_games:
        x = sravnenie(games, plays)
        for i in x:
            print(i)
