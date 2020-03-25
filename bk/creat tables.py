import sqlite3

conn = sqlite3.connect("books.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE fonbet
                  (date, time, team1, team2, win1, draw, win2, wd1, ww12, wd2)""")
conn.commit()

cursor.execute("""CREATE TABLE xstavka
                  (date, time, team1, team2, win1, draw, win2, wd1, ww12, wd2)""")
conn.commit()

cursor.execute("""CREATE TABLE liga
                  (date, time, team1, team2, win1, draw, win2)""")
conn.commit()

#cursor.execute("""CREATE TABLE winline
#                  (date, time, team1, team2, win1, draw, win2)""")
conn.commit()

cursor.execute("""CREATE TABLE pari
                  (date, time, team1, team2, win1, draw, win2)""")
conn.commit()

cursor.execute("""CREATE TABLE tennisi
                  (date, time, team1, team2, win1, draw, win2, wd1, ww12, wd2)""")
conn.commit()

cursor.execute("""CREATE TABLE city
                  (date, time, team1, team2, win1, draw, win2, wd1, ww12, wd2)""")
conn.commit()

cursor.execute("""CREATE TABLE minicity
                  (date, time, team1, team2, win1, draw, win2)""")
conn.commit()