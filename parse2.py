import bs4
import requests
import sqlite3

MINIURL = "https://m.kedem.ru"
URL = "https://m.kedem.ru/recipe/"
db_file = f"C://Users/admin/forparse/recipes.db"


def get_urls(url, miniurl):
    r = requests.get(url)
    r = r.text
    soup = bs4.BeautifulSoup(r, "html.parser")
    soup = soup.find_all('a', class_="menupage")
    for link in soup:
        u = link.get('href')
        u = miniurl + u
        yield u


def get_htmls(u, miniurl):
    num = 1
    while True:
        url = u + str(num)
        try:
            r = requests.get(url)
            r = r.text
            soup = bs4.BeautifulSoup(r, "html.parser")
            htmls = soup.find_all("a", class_="recipeblocktext")
            for html in htmls:
                link = html.get("href")
                link = miniurl + link
                response = requests.get(link)
                yield response.text
            num += 1
        except:
            print("error")
            break


def get_photo(item, MINIURL):
    url_photo = item.find("a", class_="w-lightbox w-inline-block")
    link_photo = url_photo.get('href')
    link_photo = MINIURL + link_photo
    return link_photo


def get_recipe_instructions(item):
    instructions = item.find_all("p", class_="pmargin")
    instrs = []
    for instruction in instructions:
        instrs.append(instruction.get_text())
    return instrs


def get_content(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="recipesblock")
    recipe = {}
    for item in items:
        recipe["NAME"] = item.find("h1", class_="h1").get_text()
        recipe["ingridients"] = item.find("div", class_="ringredients").get_text().strip().replace("\n", " ")
        recipe["recipeinstructions"] = get_recipe_instructions(item)
        recipe["photo"] = get_photo(item, MINIURL)
        yield recipe

        
def parse():
    for url in get_urls(URL, MINIURL):
        for html in get_htmls(url, MINIURL):
            for recipe in get_content(html):
                conn = create_connect(db_file)
                put_to_db(conn, recipe)


def create_connect(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn


def put_to_db(conn, recipe):
    recipe = [str(recipe["NAME"]), str(recipe["ingridients"]), str(recipe["recipeinstructions"]), str(recipe["photo"])]
    sql = ''' INSERT INTO recipes(name, ingridients, recipeinstructions, photo)
                 VALUES(?,?,?, ?) '''
    cursor = conn.cursor()
    cursor.execute(sql, recipe)
    print(recipe)
    conn.commit()
    conn.close()


if __name__ == "__main__":

    parse()





