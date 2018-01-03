import random
from bs4 import BeautifulSoup
from urllib.request import urlopen

base_url = "https://icook.tw"
#manu
rice_url = "https://icook.tw/categories/46"
noodle_url = "https://icook.tw/categories/360"
cake_url = "https://icook.tw/categories/16"
cookie_url = "https://icook.tw/categories/17"
url_list = []

def recipe(eat):
    if eat == "noodle":
        choose_url = noodle_url
    elif eat == "rice":
        choose_url = rice_url
    elif eat == "cookie":
        choose_url = cookie_url
    elif eat == "cake":
        choose_url = cake_url
    manu_html = urlopen(choose_url).read().decode('utf-8')
    manu = BeautifulSoup(manu_html,features='lxml')
    LIST = manu.find_all("div", {"class":"pull-left"})
    for recipe_name in LIST:
        recipe_name = base_url + recipe_name.find('a').get('href')
        #print(recipe_name)
        url_list.append(recipe_name)
#step
def cook(update):
    global url_list
    choose = random.randrange(len(url_list))
    html = urlopen(url_list[choose]).read().decode('utf-8')
    soup = BeautifulSoup(html,features='lxml')
    STEP = soup.find_all("div",{"class":"media-body"})
    INGREDIENT = soup.find_all("div",{"class":"clearfix ingredient"})
    PIC = soup.find_all("div", {"class":"picture-frame"})
    for pic in PIC:
        pic_url = pic.find('a').get('href')
        update.message.reply_text(pic_url)
    update.message.reply_text(soup.title.text)
    update.message.reply_text("\n食材:")
    for ingredient in INGREDIENT:
        text = ingredient.get_text()
        text = ''.join([t for t in text if t != '\n'])
        update.message.reply_text(text)
    update.message.reply_text("\n步驟:")
    for step in STEP:
        if '1'<=step.get_text()[0]<='9' :
            update.message.reply_text(step.get_text())
    url_list = []
