import telebot
from aiogram import Bot, Dispatcher, executor, types
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import re
import lxml

ua = UserAgent()
header = {
    "Accept": "*/*",
    "User-Agent": ua.random
}

url = "https://brawlify.com/"
r = requests.get(url, headers=header).text
soup = BeautifulSoup(r, 'lxml')

# with open('site.html', 'w', encoding='utf-8') as file:
#     file.write(r)


# Метод start
hello_title = soup.find('h1', class_='display-3 title-left mb-2 shadow-normal').text
# Удаляем цифры из строки
new_hello_title = re.sub("[0-9]", "", hello_title)

all = []
all_rating = []

bot_token = '5872111527:AAEkZKAdzQ8mcJwVrZbsvrorEK4YXhgX8cI'
bot = Bot(bot_token)
dp = Dispatcher(bot)


def get_Map(i):
    map_rem = all[i].get('Map').replace(" ", "-")
    url_map = f'https://brawlify.com/maps/detail/{map_rem}'
    r2 = requests.get(url_map, headers=header).text
    soup_map = BeautifulSoup(r2, 'lxml')
    img = soup_map.find('img', class_='img-fluid map-detail pb-4 lazyload')
    return img


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    hello_title = soup.find('h1', class_='display-3 title-left mb-2 shadow-normal').text
    # Удаляем цифры из строки
    new_hello_title = re.sub("[0-9]", "", hello_title)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btnStart = types.KeyboardButton(new_hello_title)
    btnStatistics = types.KeyboardButton("Rating Brawlers")
    markup.add(btnStart, btnStatistics)
    await bot.send_message(message.chat.id, text="Нажми на кнопку и узнай свежую мету!", reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def func(message):
    if (message.text == "Daily Meta"):
        # Метод получения списка Эвентов, Карт и бравлеров
        try:
            events = soup.find(id='active').find_all(class_='d-flex flex-column mb-3 col-sm-12 col-md-6')
            for item in events:
                event = item.find(class_='link opacity event-title-gamemode').text
                map = item.find(class_='link opacity event-title-text event-title-map mb-0').text
                brawlers_1 = item.find(class_='link event-brl event-brl-img opacity mb-1 mx-1')
                brawlers_2 = item.find(class_='link event-brl event-brl-img opacity mb-1 mx-1').find_next_sibling()
                brawlers_3 = item.find(
                    class_='link event-brl event-brl-img opacity mb-1 mx-1').find_next_sibling().find_next_sibling()
                brawlers_rate_1 = item.find(class_='link event-brl event-brl-img opacity mb-1 mx-1').text.strip()
                brawlers_rate_2 = item.find(
                    class_='link event-brl event-brl-img opacity mb-1 mx-1').find_next_sibling().text.strip()
                brawlers_rate_3 = item.find(
                    class_='link event-brl event-brl-img opacity mb-1 mx-1').find_next_sibling().find_next_sibling().text.strip()
                data = {
                    'Event': event,
                    'Map': map,
                    'Brawler_1': brawlers_1.get('title'),
                    'Win Rate_1': brawlers_rate_1,
                    'Brawler_2': brawlers_2.get('title'),
                    'Win Rate_2': brawlers_rate_2,
                    'Brawler_3': brawlers_3.get('title'),
                    'Win Rate_3': brawlers_rate_3
                }
                all.append(data)
        except:
            print("Error, check log!")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnBack = types.KeyboardButton('Назад')
        buttons = []
        for i in soup.find(id='active').find_all(class_='link opacity event-title-gamemode'):
            if i.get_text() != 'DUO SHOWDOWN':
                buttons.append(i.get_text())
        new_buttons = list(set(buttons))
        markup.add(*new_buttons, btnBack)
        await bot.send_message(message.chat.id, text="Выберите режим: ", reply_markup=markup)



    if (message.text == "SOLO SHOWDOWN"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnAfterClick = types.KeyboardButton("Daily Meta")
        markup.add(btnAfterClick)
        for i in range(len(all)):
            if all[i].get('Event') == 'SOLO SHOWDOWN':
                img_map = get_Map(i)
                await bot.send_photo(message.chat.id, img_map.get('data-src'))
                await bot.send_message(message.chat.id, text="*Режим:* " + all[i].get('Event').replace('SOLO',
                                                                                                       '').strip() + "\n" + "*Карта:* " +
                                                             all[i].get(
                                                                 'Map') + "\n" + "*Топ 3 Бравлера:* " + "\n" +
                                                             all[i].get('Brawler_1') + " " + all[i].get(
                    'Win Rate_1') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_2') + " " + all[i].get('Win Rate_2') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_3') + " " +
                                                             all[i].get('Win Rate_3') + " - *win rate*",
                                       reply_markup=markup, parse_mode="Markdown")
        all.clear()

    if (message.text == "GEM GRAB"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnAfterClick = types.KeyboardButton("Daily Meta")
        markup.add(btnAfterClick)
        for i in range(len(all)):
            if all[i].get('Event') == 'GEM GRAB':
                img_map = get_Map(i)
                await bot.send_photo(message.chat.id, img_map.get('data-src'))
                await bot.send_message(message.chat.id, text="*Режим:* " + all[i].get('Event').replace('SOLO',
                                                                                                       '').strip() + "\n" + "*Карта:* " +
                                                             all[i].get(
                                                                 'Map') + "\n" + "*Топ 3 Бравлера:* " + "\n" +
                                                             all[i].get('Brawler_1') + " " + all[i].get(
                    'Win Rate_1') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_2') + " " + all[i].get('Win Rate_2') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_3') + " " +
                                                             all[i].get('Win Rate_3') + " - *win rate*",
                                       reply_markup=markup, parse_mode="Markdown")
        all.clear()

    if (message.text == "BRAWL BALL"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnAfterClick = types.KeyboardButton("Daily Meta")
        markup.add(btnAfterClick)
        for i in range(len(all)):
            if all[i].get('Event') == 'BRAWL BALL':
                img_map = get_Map(i)
                await bot.send_photo(message.chat.id, img_map.get('data-src'))
                await bot.send_message(message.chat.id, text="*Режим:* " + all[i].get('Event').replace('SOLO',
                                                                                                       '').strip() + "\n" + "*Карта:* " +
                                                             all[i].get(
                                                                 'Map') + "\n" + "*Топ 3 Бравлера:* " + "\n" +
                                                             all[i].get('Brawler_1') + " " + all[i].get(
                    'Win Rate_1') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_2') + " " + all[i].get('Win Rate_2') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_3') + " " +
                                                             all[i].get('Win Rate_3') + " - *win rate*",
                                       reply_markup=markup, parse_mode="Markdown")
        all.clear()

    if (message.text == "BOUNTY"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnAfterClick = types.KeyboardButton("Daily Meta")
        markup.add(btnAfterClick)
        for i in range(len(all)):
            if all[i].get('Event') == 'BOUNTY':
                img_map = get_Map(i)
                await bot.send_photo(message.chat.id, img_map.get('data-src'))
                await bot.send_message(message.chat.id, text="*Режим:* " + all[i].get('Event').replace('SOLO',
                                                                                                       '').strip() + "\n" + "*Карта:* " +
                                                             all[i].get(
                                                                 'Map') + "\n" + "*Топ 3 Бравлера:* " + "\n" +
                                                             all[i].get('Brawler_1') + " " + all[i].get(
                    'Win Rate_1') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_2') + " " + all[i].get('Win Rate_2') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_3') + " " +
                                                             all[i].get('Win Rate_3') + " - *win rate*",
                                       reply_markup=markup, parse_mode="Markdown")
        all.clear()

    if (message.text == "KNOCKOUT"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnAfterClick = types.KeyboardButton("Daily Meta")
        markup.add(btnAfterClick)
        for i in range(len(all)):
            if all[i].get('Event') == 'KNOCKOUT':
                img_map = get_Map(i)
                await bot.send_photo(message.chat.id, img_map.get('data-src'))
                await bot.send_message(message.chat.id, text="*Режим:* " + all[i].get('Event').replace('SOLO',
                                                                                                       '').strip() + "\n" + "*Карта:* " +
                                                             all[i].get(
                                                                 'Map') + "\n" + "*Топ 3 Бравлера:* " + "\n" +
                                                             all[i].get('Brawler_1') + " " + all[i].get(
                    'Win Rate_1') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_2') + " " + all[i].get('Win Rate_2') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_3') + " " +
                                                             all[i].get('Win Rate_3') + " - *win rate*",
                                       reply_markup=markup, parse_mode="Markdown")
        all.clear()

    if (message.text == "HEIST"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnAfterClick = types.KeyboardButton("Daily Meta")
        markup.add(btnAfterClick)
        for i in range(len(all)):
            if all[i].get('Event') == 'HEIST':
                img_map = get_Map(i)
                await bot.send_photo(message.chat.id, img_map.get('data-src'))
                await bot.send_message(message.chat.id, text="*Режим:* " + all[i].get('Event').replace('SOLO',
                                                                                                       '').strip() + "\n" + "*Карта:* " +
                                                             all[i].get(
                                                                 'Map') + "\n" + "*Топ 3 Бравлера:* " + "\n" +
                                                             all[i].get('Brawler_1') + " " + all[i].get(
                    'Win Rate_1') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_2') + " " + all[i].get('Win Rate_2') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_3') + " " +
                                                             all[i].get('Win Rate_3') + " - *win rate*",
                                       reply_markup=markup, parse_mode="Markdown")
        all.clear()

    if (message.text == "HOT ZONE"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnAfterClick = types.KeyboardButton("Daily Meta")
        markup.add(btnAfterClick)
        for i in range(len(all)):
            if all[i].get('Event') == 'HOT ZONE':
                img_map = get_Map(i)
                await bot.send_photo(message.chat.id, img_map.get('data-src'))
                await bot.send_message(message.chat.id, text="*Режим:* " + all[i].get('Event').replace('SOLO',
                                                                                                       '').strip() + "\n" + "*Карта:* " +
                                                             all[i].get(
                                                                 'Map') + "\n" + "*Топ 3 Бравлера:* " + "\n" +
                                                             all[i].get('Brawler_1') + " " + all[i].get(
                    'Win Rate_1') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_2') + " " + all[i].get('Win Rate_2') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_3') + " " +
                                                             all[i].get('Win Rate_3') + " - *win rate*",
                                       reply_markup=markup, parse_mode="Markdown")
        all.clear()

    if (message.text == "ROBO RUMBLE"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnAfterClick = types.KeyboardButton("Daily Meta")
        markup.add(btnAfterClick)
        for i in range(len(all)):
            if all[i].get('Event') == 'ROBO RUMBLE':
                img_map = get_Map(i)
                await bot.send_photo(message.chat.id, img_map.get('data-src'))
                await bot.send_message(message.chat.id, text="*Режим:* " + all[i].get('Event').replace('SOLO',
                                                                                                       '').strip() + "\n" + "*Карта:* " +
                                                             all[i].get(
                                                                 'Map') + "\n" + "*Топ 3 Бравлера:* " + "\n" +
                                                             all[i].get('Brawler_1') + " " + all[i].get(
                    'Win Rate_1') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_2') + " " + all[i].get('Win Rate_2') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_3') + " " +
                                                             all[i].get('Win Rate_3') + " - *win rate*",
                                       reply_markup=markup, parse_mode="Markdown")
        all.clear()

    if (message.text == "DUELS"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnAfterClick = types.KeyboardButton("Daily Meta")
        markup.add(btnAfterClick)
        for i in range(len(all)):
            if all[i].get('Event') == 'DUELS':
                img_map = get_Map(i)
                await bot.send_photo(message.chat.id, img_map.get('data-src'))
                await bot.send_message(message.chat.id, text="*Режим:* " + all[i].get('Event').replace('SOLO',
                                                                                                       '').strip() + "\n" + "*Карта:* " +
                                                             all[i].get(
                                                                 'Map') + "\n" + "*Топ 3 Бравлера:* " + "\n" +
                                                             all[i].get('Brawler_1') + " " + all[i].get(
                    'Win Rate_1') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_2') + " " + all[i].get('Win Rate_2') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_3') + " " +
                                                             all[i].get('Win Rate_3') + " - *win rate*",
                                       reply_markup=markup, parse_mode="Markdown")
        all.clear()

    if (message.text == "PAYLOAD"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnAfterClick = types.KeyboardButton("Daily Meta")
        markup.add(btnAfterClick)
        for i in range(len(all)):
            if all[i].get('Event') == 'PAYLOAD':
                img_map = get_Map(i)
                await bot.send_photo(message.chat.id, img_map.get('data-src'))
                await bot.send_message(message.chat.id, text="*Режим:* " + all[i].get('Event').replace('SOLO',
                                                                                                       '').strip() + "\n" + "*Карта:* " +
                                                             all[i].get(
                                                                 'Map') + "\n" + "*Топ 3 Бравлера:* " + "\n" +
                                                             all[i].get('Brawler_1') + " " + all[i].get(
                    'Win Rate_1') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_2') + " " + all[i].get('Win Rate_2') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_3') + " " +
                                                             all[i].get('Win Rate_3') + " - *win rate*",
                                       reply_markup=markup, parse_mode="Markdown")
        all.clear()

    if (message.text == "WIPEOUT"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnAfterClick = types.KeyboardButton("Daily Meta")
        markup.add(btnAfterClick)
        for i in range(len(all)):
            if all[i].get('Event') == 'WIPEOUT':
                img_map = get_Map(i)
                await bot.send_photo(message.chat.id, img_map.get('data-src'))
                await bot.send_message(message.chat.id, text="*Режим:* " + all[i].get('Event').replace('SOLO',
                                                                                                       '').strip() + "\n" + "*Карта:* " +
                                                             all[i].get(
                                                                 'Map') + "\n" + "*Топ 3 Бравлера:* " + "\n" +
                                                             all[i].get('Brawler_1') + " " + all[i].get(
                    'Win Rate_1') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_2') + " " + all[i].get('Win Rate_2') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_3') + " " +
                                                             all[i].get('Win Rate_3') + " - *win rate*",
                                       reply_markup=markup, parse_mode="Markdown")
        all.clear()

    if (message.text == "BASKET BRAWL"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnAfterClick = types.KeyboardButton("Daily Meta")
        markup.add(btnAfterClick)
        for i in range(len(all)):
            if all[i].get('Event') == 'BASKET BRAWL':
                img_map = get_Map(i)
                await bot.send_photo(message.chat.id, img_map.get('data-src'))
                await bot.send_message(message.chat.id, text="*Режим:* " + all[i].get('Event').replace('SOLO',
                                                                                                       '').strip() + "\n" + "*Карта:* " +
                                                             all[i].get(
                                                                 'Map') + "\n" + "*Топ 3 Бравлера:* " + "\n" +
                                                             all[i].get('Brawler_1') + " " + all[i].get(
                    'Win Rate_1') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_2') + " " + all[i].get('Win Rate_2') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_3') + " " +
                                                             all[i].get('Win Rate_3') + " - *win rate*",
                                       reply_markup=markup, parse_mode="Markdown")
        all.clear()

    if (message.text == "SIEGE"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnAfterClick = types.KeyboardButton("Daily Meta")
        markup.add(btnAfterClick)
        for i in range(len(all)):
            if all[i].get('Event') == 'SIEGE':
                img_map = get_Map(i)
                await bot.send_photo(message.chat.id, img_map.get('data-src'))
                await bot.send_message(message.chat.id, text="*Режим:* " + all[i].get('Event').replace('SOLO',
                                                                                                       '').strip() + "\n" + "*Карта:* " +
                                                             all[i].get(
                                                                 'Map') + "\n" + "*Топ 3 Бравлера:* " + "\n" +
                                                             all[i].get('Brawler_1') + " " + all[i].get(
                    'Win Rate_1') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_2') + " " + all[i].get('Win Rate_2') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_3') + " " +
                                                             all[i].get('Win Rate_3') + " - *win rate*",
                                       reply_markup=markup, parse_mode="Markdown")
        all.clear()

    if (message.text == "BOSS FIGHT"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnAfterClick = types.KeyboardButton("Daily Meta")
        markup.add(btnAfterClick)
        for i in range(len(all)):
            if all[i].get('Event') == 'BOSS FIGHT':
                img_map = get_Map(i)
                await bot.send_photo(message.chat.id, img_map.get('data-src'))
                await bot.send_message(message.chat.id, text="*Режим:* " + all[i].get('Event').replace('SOLO',
                                                                                                       '').strip() + "\n" + "*Карта:* " +
                                                             all[i].get(
                                                                 'Map') + "\n" + "*Топ 3 Бравлера:* " + "\n" +
                                                             all[i].get('Brawler_1') + " " + all[i].get(
                    'Win Rate_1') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_2') + " " + all[i].get('Win Rate_2') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_3') + " " +
                                                             all[i].get('Win Rate_3') + " - *win rate*",
                                       reply_markup=markup, parse_mode="Markdown")
        all.clear()

    if (message.text == "BIG GAME"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnAfterClick = types.KeyboardButton("Daily Meta")
        markup.add(btnAfterClick)
        await bot.send_message(message.chat.id, text='*Тут все понятно*,\nДавай другой)', reply_markup=markup,
                               parse_mode="Markdown")
        all.clear()

    if (message.text == "LAST STAND"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnAfterClick = types.KeyboardButton("Daily Meta")
        markup.add(btnAfterClick)
        for i in range(len(all)):
            if all[i].get('Event') == 'LAST STAND':
                img_map = get_Map(i)
                await bot.send_photo(message.chat.id, img_map.get('data-src'))
                await bot.send_message(message.chat.id, text="*Режим:* " + all[i].get('Event').replace('SOLO',
                                                                                                       '').strip() + "\n" + "*Карта:* " +
                                                             all[i].get(
                                                                 'Map') + "\n" + "*Топ 3 Бравлера:* " + "\n" +
                                                             all[i].get('Brawler_1') + " " + all[i].get(
                    'Win Rate_1') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_2') + " " + all[i].get('Win Rate_2') + " - *win rate*" + "\n" + all[i].get(
                    'Brawler_3') + " " +
                                                             all[i].get('Win Rate_3') + " - *win rate*",
                                       reply_markup=markup, parse_mode="Markdown")
        all.clear()

    if (message.text == "Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttonToBack = types.KeyboardButton("Daily Meta")
        markup.add(buttonToBack)
        await bot.send_message(message.chat.id, text="Выберите режим: ", reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dp)
