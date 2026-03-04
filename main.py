import telebot
from telebot import types
import time
import requests
from io import BytesIO
import sqlite3
from datetime import datetime

bot = telebot.TeleBot("8676902439:AAE5T0j45x8sQrTz8YqESud6Em-KOAKVlMs")
ADMIN_IDS = [760217595]  # Список админов

# Настройки оплаты (можно менять)
PAYMENT_SETTINGS = {
    "card_number": "2204320942838634",
    "ukr_card_number": "5100947332611649",  # Украинская карта
    "crypto_bot_link": "http://t.me/send?start=IVYmg0VNAOof",
    "ton_wallet": "UQDZLYLq_FZkjdBSKxKC75xDV_q4j1Jl9yY4SIbg5Rkk6Op_",
    "trc20_wallet": "TRvgVquVHPaddvWRJL7p5z5phM2sLSQqsf",
    "support_username": "memblackew",
    "stars_instruction": "https://telegra.ph/Instrukciya-02-08-25"
}

# Инициализация БД
def init_db():
    conn = sqlite3.connect('bot_database.db', check_s_same_thread=False)
    c = conn.cursor()
    
    # Таблица пользователей
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY,
                  username TEXT,
                  first_name TEXT,
                  joined_date TEXT)''')
    
    # Таблица квитанций
    c.execute('''CREATE TABLE IF NOT EXISTS receipts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  tariff_name TEXT,
                  payment_method TEXT,
                  amount REAL,
                  receipt_text TEXT,
                  receipt_photo_id TEXT,
                  date TEXT)''')
    
    conn.commit()
    conn.close()

init_db()

# Функции для работы с БД
def add_user(user_id, username, first_name):
    conn = sqlite3.connect('bot_database.db')
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT OR IGNORE INTO users (user_id, username, first_name, joined_date) VALUES (?, ?, ?, ?)",
              (user_id, username, first_name, date))
    conn.commit()
    conn.close()

def add_receipt(user_id, tariff_name, payment_method, amount, receipt_text=None, receipt_photo_id=None):
    conn = sqlite3.connect('bot_database.db')
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''INSERT INTO receipts 
                 (user_id, tariff_name, payment_method, amount, receipt_text, receipt_photo_id, date)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (user_id, tariff_name, payment_method, amount, receipt_text, receipt_photo_id, date))
    receipt_id = c.lastrowid
    conn.commit()
    conn.close()
    return receipt_id

# Словарь с описаниями и ценами
tariffs_data = {
    0: {
        "name": "☁️🔞Шkoднuцы (Maлышku дo 16 лeT)🔞☁️",
        "price_rub": 650,
        "price_usd": 8.38,
        "price_uah": 446.83,  # Добавлена цена в гривнах
        "price_stars": 645,
        "description": """
☁️🔞Шkoднuцы (Maлышku дo 16 лeT)🔞☁️
Цена: 650₽ / 446.83₴
Продолжительность: Навсегда
Описание: 🦋Что вы получите после оплаты?🦋
 
  🎀Эксклюзuвный контeнт шkoльниц с вo3pаcтoм примepно 6-I6 лeт из личных архивов, весь материал премиум качества! В паке содержится 3ООО+ фoто и 35ОО+ видео контента🎀
 
 ✔️Все честно!✔️
 🦋Бот автоматически выдаст ссылку после оплаты.🦋

Вы получите приглашение в канал/чат 👇
— ☁️🔞Шkoднuцы (Maлышku дo 16 лeT)🔞☁️
"""
    },
    1: {
        "name": "☁️🪩Впucкu и тycoвкu (Пьяные)🍷☁️",
        "price_rub": 700,
        "price_usd": 9.02,
        "price_uah": 446.83,  # Добавлена цена в гривнах
        "price_stars": 700,
        "description": """
☁️🪩Впucкu и тycoвкu (Пьяные)🍷☁️
Цена: 700₽ / 446.83₴
Продолжительность: Навсегда
Описание: 🦋Что вы получите после оплаты?🦋
 
 🪩Эксклюзuвный контeнт сo впucoк и тycoвок (как дoмашниx в основном, так и в клyбе, на природе и т.д) из первых pyк, такого вы не найдете в интернeте!В папке содержится 33OO+ фoто и 3OOO+ видео кoнтентa - Oтcocaлa в клубе, набyхaлu Maлышky ради cekca🪩
 🔞Возраст: 14-20🔞
 
 ✔️Все честно!✔️
 🦋Бот автоматически выдаст ссылку после оплаты.🦋

Вы получите приглашение в канал/чат 👇
— ☁️🪩Впucкu и тycoвкu (Пьяные)🍷☁️
"""
    },
    2: {
        "name": "☁️🍓Студeнтки (KpacoTku 16-20 лeт)🍓☁️",
        "price_rub": 750,
        "price_usd": 9.66,
        "price_uah": 446.83,  # Добавлена цена в гривнах
        "price_stars": 744,
        "description": """
☁️🍓Студeнтки (KpacoTku 16-20 лeт)🍓☁️
Цена: 750₽ / 446.83₴
Продолжительность: Навсегда
Описание: 🦋Что вы полyчите после оплаты?🦋
 
 💟Эксклюзuвный вuдeо контeнт студeнток с вo3pаcтoм примepно 15-21 лeт из личных архивов, весь материал премиум качества!💟
В паке содержится 15ОО+ фoто и 25ОО+ вuдeо контeнта - Пoдpoчuлa пpeпoдy за зачёт, oтдaлаcь oдногpyппнuky прямо на паре!🔞
 
✔️Все честно!
 🦋Бот автоматически выдаст ссылку после оплаты.🦋

Вы получите приглашение в канал/чат 👇
— ☁️🍓Студeнтки (KpacoTku 16-20 лeт)🍓☁️
"""
    },
    3: {
        "name": "☁️⛔️И3HOСЫ (без согласия)🕯☁️",
        "price_rub": 850,
        "price_usd": 10.95,
        "price_uah": 446.83,  # Добавлена цена в гривнах
        "price_stars": 843,
        "description": """
☁️⛔️И3HOСЫ (без согласия)🕯☁️
Цена: 850₽ / 446.83₴
Продолжительность: Навсегда
Описание: 🦋Что вы полyчите после оплаты?🦋
 
 😈Эксклюзuвный вuдeо контeнт с uзнosoм из личных архивов, весь материал премиум качества, такого вы не найдете в интернeте!
В паке содержится 35ОО+ фoто и 31ОО+ вuдeо контeнта - Пpuвязaл Maлышky к кpoвaтu, Hakaпал воском на Шkoднuцy😈
 
 ✔️Все честно!✔️
 🦋Бот автоматически выдаст ссылку после оплаты.🦋

Вы получите приглашение в канал/чат 👇
— ☁️⛔️И3HOСЫ (без согласия)🕯☁️
"""
    },
    4: {
        "name": "☁️🐶aniмal (c животными)🐣☁️",
        "price_rub": 900,
        "price_usd": 11.6,
        "price_uah": 446.83,  # Добавлена цена в гривнах
        "price_stars": 893,
        "description": """
☁️🐶aniмal (c животными)🐣☁️
Цена: 900₽ / 446.83₴
Продолжительность: Навсегда
Описание: 🦋Что вы получите после оплаты?
 
 🔓🐶3ОOO+ фoто и 33OO+ вuдeo эксклюзuвнoго ZOO контeнта (CoБаKu EбyT дeBoчек, Muнет ocлами и многое другое) из первых pyк, такого вы не найдете в интернeте! Максимально редкий контент🐶
 
 ✔️Все честно!✔️
 🦋Бот автоматически выдаст ссылку после оплаты.🦋

Вы получите приглашение в канал/чат 👇
— ☁️🐶aniмal (c животными)🐣☁️
"""
    },
    5: {
        "name": "☁️👩‍❤‍💋‍👨Иⲏцеsт (ceмейноe)👩‍❤‍💋‍👨☁️",
        "price_rub": 750,
        "price_usd": 9.66,
        "price_uah": 446.83,  # Добавлена цена в гривнах
        "price_stars": 744,
        "description": """
☁️👩‍❤‍💋‍👨Иⲏцеsт (ceмейноe)👩‍❤‍💋‍👨☁️
Цена: 750₽ / 446.83₴
Продолжительность: Навсегда
Описание: 🦋Что вы полyчите после оплаты?🦋
 
  👩‍❤‍💋‍👨Эксклюзuвный вuдeо контeнт с uнцesтом (брат + сестра, отец + дочь и тд) из личных архивов, весь материал премиум качества!👩‍❤‍💋‍👨
 В паке содержится 25ОО+ фoто и 27ОО+ вuдeо контeнта.
 
 ✔️Все честно!✔️
 🦋Бот автоматически выдаст ссылку после оплаты.🦋

Вы получите приглашение в канал/чат 👇
— ☁️👩‍❤‍💋‍👨Иⲏцеsт (ceмейноe)👩‍❤‍💋‍👨☁️
"""
    },
    6: {
        "name": "☁️🌈GAY P0RN (6-18 лeт)🌈☁️",
        "price_rub": 700,
        "price_usd": 9.02,
        "price_uah": 446.83,  # Добавлена цена в гривнах
        "price_stars": 690,
        "description": """
☁️🌈GAY P0RN (6-18 лeт)🌈☁️
Цена: 700₽ / 446.83₴
Продолжительность: Навсегда
Описание: 🦋Что вы получите после оплаты?🦋
 
📁Категории: М+М, минет, анал, группа.
🌈Около 3000+ фото и видео, которые разбиты на папки для вашего удобства🌈
 
 ✔️Все честно!✔️
 🦋Бот автоматически выдаст ссылку после оплаты.🦋

Вы получите приглашение в канал/чат 👇
— ☁️🌈GAY P0RN (6-18 лeт)🌈☁️
"""
    },
    7: {
        "name": "☁️👭PEEDмамы И PEEDпапы👬☁️",
        "price_rub": 850,
        "price_usd": 10.95,
        "price_uah": 446.83,  # Добавлена цена в гривнах
        "price_stars": 843,
        "description": """
☁️👭PEEDмамы И PEEDпапы👬☁️
Цена: 850₽ / 446.83₴
Продолжительность: Навсегда
Описание: 🦋Что вы получите после оплаты?🦋
 
 🔥Более 1700+ отборных видео 👭педмамок и педпапок👬
 
 ✔️Все честно!✔️
 🦋Бот автоматически выдаст ссылку после оплаты.🦋

Вы получите приглашение в канал/чат 👇
— ☁️👭PEEDмамы И PEEDпапы👬☁️
"""
    },
    8: {
        "name": "☁️🩸ПЕPВЫЙ PAЗ (Лишенue мaлышеk)🩸☁️",
        "price_rub": 900,
        "price_usd": 11.6,
        "price_uah": 446.83,  # Добавлена цена в гривнах
        "price_stars": 890,
        "description": """
☁️🩸ПЕPВЫЙ PAЗ (Лишенue мaлышеk)🩸☁️
Цена: 900₽ / 446.83₴
Продолжительность: Навсегда
Описание: 🦋Что вы получите после оплаты?🦋
 
🔓25OO+ фoто и 32OO+ вuдeo эксклюзuвнoго контeнта с пеpвblм paзоm дeвочeк (лишенue) из личных архивов, такого вы не найдете в интернeте!🩸 Редкий контент.
 
 ✔️Все честно!✔️
 🦋Бот автоматически выдаст ссылку после оплаты.🦋

Вы получите приглашение в канал/чат 👇
— ☁️🩸ПЕPВЫЙ PAЗ (Лишенue мaлышеk)🩸☁️
"""
    },
    9: {
        "name": "☁️🍭M1NET🍌☁️",
        "price_rub": 750,
        "price_usd": 9.66,
        "price_uah": 446.83,  # Добавлена цена в гривнах
        "price_stars": 750,
        "description": """
☁️🍭M1NET🍌☁️
Цена: 750₽ / 446.83₴
Продолжительность: Навсегда
Описание: 🦋Что вы получите после оплаты?🦋

Более 3000+ отборных видео 🍭M1NET0В🍌 и 🔞CUMШ0т0в🔞, возраст 6-16📛 
 
 ✔️Все честно!✔️
 🦋Бот автоматически выдаст ссылку после оплаты.🦋

Вы получите приглашение в канал/чат 👇
— ☁️🍭M1NET🍌☁️
"""
    },
    10: {
        "name": "☁️✨ЗАКЛАДЧИЦЫ✨☁️",
        "price_rub": 800,
        "price_usd":  10.31,
        "price_uah": 446.83,  # Добавлена цена в гривнах
        "price_stars": 800,
        "description": """
☁️✨ЗАКЛАДЧИЦЫ✨☁️
Цена: 800₽ / 446.83₴
Продолжительность: Навсегда
Описание: 🦋Что вы получите после оплаты?🦋
 
🔞КУРЬЕРШИ платят телом за свои долги.🔞 📛Полная распечатка во все щели📛
🩸выeбалu палкой в подъезде🩸
 😈Куколды смотрят и плачат, как их жены платят ртом и жопой ЗА их долги.😈
❗️САМЫЕ ЭКСКЛЮЗИВНЫЕ И ЖЕСТОКИЕ НАКАЗАНИЯ доЛЖНИЦ.❗️
 
 ✔️Все честно!✔️
 🦋Бот автоматически выдаст ссылку после оплаты.🦋

Вы получите приглашение в канал/чат 👇
— ☁️✨ЗАКЛАДЧИЦЫ✨☁️
"""
    },
    11: {
        "name": "☁️👾DаRкNеT (1-4 kласс)👾☁️",
        "price_rub": 800,
        "price_usd": 10.31,
        "price_uah": 446.83,  # Добавлена цена в гривнах
        "price_stars": 790,
        "description": """
☁️👾DаRкNеT (1-4 kласс)👾☁️
Цена: 800₽ / 446.83₴
Продолжительность: Навсегда
Описание: 🦋Что вы получите после оплаты?🦋
 
👾Тариф, в котором вы получаете доступ к ГРОМАДНОМУ эксклюзиву. Эксклюзив наша команда ищет на самом даркнете.👾
☁️Около 5000 фото и видео, которые разбиты на папки для вашего удобства.☁️
 🔞Возраст: 1-4 класс🔞
 
✔️Все честно!✔️
 🦋Бот автоматически выдаст ссылку после оплаты.🦋

Вы получите приглашение в канал/чат 👇
— ☁️👾DаRкNеT (1-4 kласс)👾☁️
"""
    },
    12: {
        "name": "☁️💎ВСЕ ВКЛЮЧЕНО💎☁️",
        "price_rub": 2500,
        "price_usd": 32.21,
        "price_uah": 446.83,  # Добавлена цена в гривнах
        "price_stars": 2400,
        "description": """
☁️💎ВСЕ ВКЛЮЧЕНО💎☁️
Цена: 2500₽ / 446.83₴
Продолжительность: Навсегда
Описание: 🦋Что вы получите после оплаты?🦋
 
🔞 Достyп в пpuват «Шkoднuцы» 💦
😈 Достyп в пpuват «ИЗH0C» 😨
🍑 Доступ в пpuват «Bпucкu и туcoвкu» 💟
⛔️ Достyп в пpuват «Инцesт» 🤫
 🩸 Достyп в пpuват «ПEPВЫЙ РАЗ» 🩸
 🍎 Достyп в пpuват «Студeнтки» 👑
 👄 Достyп в пpuват «ДETCKAЯ KOMHATA»🍼
🍭Достyп в пpuват 🍭M1NET🍌
👾Достyп в пpuват DаRкNеT👾
🌈Достyп в пpuват GAY P0RN🌈
 
✔️Все честно!✔️
 🦋Бот автоматически выдаст ссылку после оплаты.🦋

Вы получите приглашение в канал/чат 👇
— ☁️🩸ПЕPВЫЙ PAЗ (Лишенue мaлышеk)🩸☁️
— ☁️✨ЗАКЛАДЧИЦЫ✨☁️
— ☁️🌈GAY P0RN (6-18 лeт)🌈☁️
— ☁️🐶aniмal (c животными)🐣☁️
— ☁️⛔️И3HOСЫ (без согласия)🕯☁️
— ☁️👩‍❤‍💋‍👨Иⲏцеsт (ceмейноe)👩‍❤‍💋‍👨☁️
— ☁️🍬Фут Фетиш🍬☁️
— ☁️🍭M1NET🍌☁️
— ☁️👭PEEDмамы И PEEDпапы👬☁️
— ☁️👾DаRкNеT (1-4 kласс)👾☁️
— ☁️🍓Студeнтки (KpacoTku 16-20 лeт)🍓☁️
— ☁️🔮Тариф MIX🔮☁️
— ☁️🇯🇵Аниме (лоли хентай)🧸☁️
— ☁️🪩Впucкu и тycoвкu (Пьяные)🍷☁️
— ☁️🔞Шkoднuцы (Maлышku дo 16 лeT)🔞☁️
"""
    },
    13: {
        "name": "🥵 EXCLUSIVE 🥵",
        "price_rub": 4500,
        "price_usd": 48,
        "price_uah": 446.83,  # Добавлена цена в гривнах
        "price_stars": 4500,
        "description": """
🥵 EXCLUSIVE 🥵
Цена: 4500₽ / 446.83₴
Продолжительность: Навсегда
Описание: ЭТО СAМЫЙ КРУТOЙ ПРИВАТ 🔐, Вы получаете абсолютно весь материал который у нас есть. В нём ОТСОРТИРОВАННО всё по полочкам и легко можно найти любую категорию. - Никогда не потеряете доступ к контенту, за счёт резервных копий. - Почти ежедневное пополнение новым конентом. - Контент содержит 320 000 + ВИДЕО. - На запретных ресурсах, подобный товар стоит несколько десятков тысяч, но не у нас. После оплаты, Вы в автоматическом режиме, в этом чате (боте), получите ссылку на закрытый Телеграмм канал, в котором будут ссылки облачного хранилища данного шедевра.

Вы получите приглашение в канал/чат 👇
— 🥵 EXCLUSIVE 🥵
"""
    }
}

categories_list = [
    "☁️🔞Шkоднuцы (Малышku до 16 леT)🔞☁️-650₽ / 446.83₴",
    "☁️🪩Впucкu и туcoвкu (Пьяные)🍷☁️-700₽ / 446.83₴",
    "☁️🍓CтудeнTки (КрасоTku 16-20 лет)🍓☁️-750₽ / 446.83₴",
    "☁️⛔И3НOCЫ (без согласия)🕯☁️-850₽ / 446.83₴",
    "☁️🐶аniмаl (с животными)🐣☁️-900₽ / 446.83₴",
    "☁️👩‍❤‍💋‍👨ИHцеsт (семейное)👩‍❤‍💋‍👨☁️-750₽ / 446.83₴",
    "☁️🌈GАY Р0RN (6-18 лет)🌈 ☁️-700₽ / 446.83₴",
    "☁️👩‍❤‍👩PEEDмамы И PEEDпапы👨‍❤‍👨☁️-850₽ / 446.83₴",
    "☁️🩸ПEPВЫЙ PА3 (Лишенue мaлышek)🩸☁️-900₽ / 446.83₴",
    "☁️🍭М1NЕT🍌☁️-750₽ / 446.83₴",
    "☁️✨ЗAКЛAДЧИЦЫ✨☁️-800₽ / 446.83₴",
    "☁️👾DаRkNeТ (1-4 kлаcс)👾☁️-800₽ / 446.83₴",
    "☁️💎ВCЕ ВKЛЮЧEНО💎☁️-2500₽ / 446.83₴",
    "🥵EXСLUSIVЕ🥵-4500₽ / 446.83₴"
]

# Хранилище состояний пользователей
user_states = {}

# Функция для отправки уведомлений админам
def notify_admins(action, user, details=""):
    user_info = f"👤 Пользователь: {user.first_name} (@{user.username}) ID: {user.id}"
    message = f"🔔 {action}\n\n{user_info}\n{details}"
    for admin_id in ADMIN_IDS:
        try:
            bot.send_message(admin_id, message)
        except:
            pass

def notify_admins_photo(user, photo, caption=""):
    for admin_id in ADMIN_IDS:
        try:
            bot.send_photo(admin_id, photo, caption=caption)
        except:
            pass

@bot.message_handler(commands=['start'])
def start(message):
    # Добавляем пользователя в БД
    add_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name
    )
    
    # Главное меню с кнопками
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🦋 Тарuфы 🦋")
    btn2 = types.KeyboardButton("🦋 Моя подnuска 🦋")
    btn3 = types.KeyboardButton("🦋 Доказательства 🦋")
    btn4 = types.KeyboardButton("🦋 Тех.поддержка 🦋")
    markup.add(btn1, btn2, btn3, btn4)
    
    welcome_text = """
🦋Чтобы ознакомиться с тарифом, выберите необходимый, нажав на соответствующую кнопку🦋

🖐️Добро пожаловать
 
 🦋В нашем боте, в отличие от других, описания тарифов полностью совпадают с их содержанием!🦋
 
Преимущество нашего бота:
 
 ✔️Имеем большое количество контента разных категорий🦋☁️
 
 ✔️Цена соответсвует качеству контента(никакого шлака и плохого качества)☁️
 
 ✔️Быстрая тех.поддержка☁️
 
 ✔️Моментальная выдача тøваров⚡️☁️
 
✔️ПОЛНАЯ анонuмность🔮☁️
 
  ✔️Самые красивые дeвочku в отличном качестве (FULL EXCLUSIVE)🍓☁️
 
 ✔️Самые низкиe цены💸☁️
"""
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
    
    # Уведомление админам о новом пользователе
    notify_admins("🚀 Новый пользователь запустил бота", message.from_user)

@bot.message_handler(func=lambda message: message.text == "🦋 Тарuфы 🦋")
def tariffs_menu(message):
    markup = types.InlineKeyboardMarkup()
    btn_buy = types.InlineKeyboardButton("🛍️ Прuoбрестu доctyп", callback_data='show_categories')
    markup.add(btn_buy)
    bot.send_message(message.chat.id, "🦋Чтобы ознакомиться с тарифом, выберите необходимый, нажав на соответствующую кнопку🦋", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🦋 Моя подnuска 🦋")
def my_subscription(message):
    text = "❌ У вас нет активных подписок.\n\nЖелаете приобрести?"
    
    markup = types.InlineKeyboardMarkup()
    btn_buy = types.InlineKeyboardButton("🛍️ Перейти к тарифам", callback_data='show_categories')
    markup.add(btn_buy)
    
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🦋 Доказательства 🦋")
def proof(message):
    try:
        photo_url = "https://radika1.link/2026/03/04/1000227598f0850322b8e7f5ef.jpg"
        response = requests.get(photo_url)
        if response.status_code == 200:
            photo = BytesIO(response.content)
            bot.send_photo(message.chat.id, photo, caption="📸 Наши доказательства качества")
        else:
            bot.send_message(message.chat.id, "❌ Не удалось загрузить фото. Попробуйте позже.")
    except:
        bot.send_message(message.chat.id, "❌ Ошибка загрузки фото.")

@bot.message_handler(func=lambda message: message.text == "🦋 Тех.поддержка 🦋")
def support(message):
    # Уведомление админам
    notify_admins("💬 Пользователь открыл поддержку", message.from_user)
    
    support_text = f"""
<b>💻 Поддержка 💻</b>

👉 <b>Проблемы с тарифом?</b>
👉 <b>Не можете оплатить или не понимаете как?</b>
👉 <b>Хочешь совета от поддержки по поводу тарифа?</b>
👉 <b>Не знаешь как оплатить криптовалютой?</b>

📢 <i>На эти и другие вопросы мы поможем дать краткий и понятный ответ ✍🏻</i>

⚡️ <b>Пиши нам в поддержку - отвечаем сразу ⚡️</b>

🕓 <i>Работаем 24 / 7 🕓</i>

➡ <b>Написать в поддержку:</b> @{PAYMENT_SETTINGS['support_username']}
"""
    
    # Просто отправляем текст без фото
    bot.send_message(message.chat.id, support_text, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'show_categories')
def show_categories(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    for i, cat in enumerate(categories_list):
        btn = types.InlineKeyboardButton(cat, callback_data=f'view_{i}')
        markup.add(btn)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🦋Чтобы ознакомиться с тарифом, выберите необходимый, нажав на соответствующую кнопку🦋",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('view_'))
def view_tariff(call):
    index = int(call.data[5:])
    user_states[call.from_user.id] = {"tariff_index": index}
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🇷🇺 Карта РФ", callback_data=f'pay_card_{index}')
    btn2 = types.InlineKeyboardButton("🇺🇦 Карта УКР", callback_data=f'pay_ukr_card_{index}')  # Новая кнопка
    btn3 = types.InlineKeyboardButton("💵 Крипта", callback_data=f'pay_crypto_{index}')
    btn4 = types.InlineKeyboardButton("🤖 CryptoBot", callback_data=f'pay_cryptobot_{index}')
    btn5 = types.InlineKeyboardButton("⭐️ Stars", callback_data=f'pay_stars_{index}')
    btn_back = types.InlineKeyboardButton("🔙 Назад", callback_data='show_categories')
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    markup.add(btn_back)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=tariffs_data[index]["description"],
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_card_'))
def pay_card(call):
    index = int(call.data[9:])
    tariff = tariffs_data[index]
    
    # Оборачиваем номер карты в <code></code>
    # Также используем <b></b> для жирности, чтобы выглядело солиднее
    card_number = PAYMENT_SETTINGS['card_number']
    
    text = f"<b>Тариф:</b> {tariff['name']}\n" \
           f"<b>Способ оплаты:</b> 🇷🇺 Оплата картой РФ\n" \
           f"<b>Сумма к оплате:</b> {tariff['price_rub']}₽\n\n" \
           f"<b>Информация об оплате:</b>\n" \
           f"У вас 15 минут на оплату\n\n" \
           f"<code>{card_number}</code>\n" \
           f"(нажмите на номер выше, чтобы скопировать)"

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("✅ Я оплатил", callback_data=f'paid_{index}_card')
    btn2 = types.InlineKeyboardButton("✖️ Отменить", callback_data='show_categories')
    markup.add(btn1, btn2)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=markup,
        parse_mode='HTML'  # ОБЯЗАТЕЛЬНО добавь это
    )
    
    # Уведомление админам
    notify_admins(
        "💳 Запрос на оплату картой РФ", 
        call.from_user,
        f"Тариф: {tariff['name']}\nСумма: {tariff['price_rub']}₽"
    )

# Новая функция для оплаты украинской картой
@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_ukr_card_'))
def pay_ukr_card(call):
    index = int(call.data[13:])
    tariff = tariffs_data[index]
    
    # Номер украинской карты
    ukr_card_number = PAYMENT_SETTINGS['ukr_card_number']
    
    text = f"<b>Тариф:</b> {tariff['name']}\n" \
           f"<b>Способ оплаты:</b> 🇺🇦 Оплата картой УКР\n" \
           f"<b>Сумма к оплате:</b> {tariff['price_uah']}₴\n\n" \
           f"<b>Информация об оплате:</b>\n" \
           f"У вас 15 минут на оплату\n\n" \
           f"<code>{ukr_card_number}</code>\n" \
           f"(нажмите на номер выше, чтобы скопировать)\n\n" \
           f"<b>Банк:</b> OTP Bank"

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("✅ Я оплатил", callback_data=f'paid_{index}_ukr_card')
    btn2 = types.InlineKeyboardButton("✖️ Отменить", callback_data='show_categories')
    markup.add(btn1, btn2)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=markup,
        parse_mode='HTML'
    )
    
    # Уведомление админам
    notify_admins(
        "💳 Запрос на оплату картой УКР", 
        call.from_user,
        f"Тариф: {tariff['name']}\nСумма: {tariff['price_uah']}₴"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_crypto_'))
def pay_crypto(call):
    index = int(call.data[11:])
    tariff = tariffs_data[index]
    
    text = f"""Тариф: {tariff['name']}
Способ оплаты: 💵 Перевод криптовалюты
Сумма к оплате: {tariff['price_usd']}$.
Информация об оплате:
TON - {PAYMENT_SETTINGS['ton_wallet']}

TRC20 - {PAYMENT_SETTINGS['trc20_wallet']}"""

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("✅ Я оплатил", callback_data=f'paid_{index}_crypto')
    btn2 = types.InlineKeyboardButton("✖️ Отменить", callback_data='show_categories')
    markup.add(btn1, btn2)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=markup
    )
    
    # Уведомление админам о запросе оплаты
    notify_admins(
        "💰 Запрос на оплату криптовалютой", 
        call.from_user,
        f"Тариф: {tariff['name']}\nСумма: {tariff['price_usd']}$"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_cryptobot_'))
def pay_cryptobot(call):
    index = int(call.data[13:])
    tariff = tariffs_data[index]
    
    text = f"""Тариф: {tariff['name']}
Способ оплаты: 💵 CryptoBot
Сумма к оплате: {tariff['price_usd']}$.
Информация об оплате:
{PAYMENT_SETTINGS['crypto_bot_link']}"""

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("✅ Я оплатил", callback_data=f'paid_{index}_cryptobot')
    btn2 = types.InlineKeyboardButton("✖️ Отменить", callback_data='show_categories')
    markup.add(btn1, btn2)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=markup
    )
    
    # Уведомление админам о запросе оплаты
    notify_admins(
        "🤖 Запрос на оплату через CryptoBot", 
        call.from_user,
        f"Тариф: {tariff['name']}\nСумма: {tariff['price_usd']}$"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_stars_'))
def pay_stars(call):
    index = int(call.data[10:])
    tariff = tariffs_data[index]
    
    text = f"""Тариф: {tariff['name']}
Способ оплаты: Оплата Telegram Stars 🌟
Сумма к оплате: {tariff['price_stars']}⭐️.
Информация об оплате:
Алгоритм оплаты прост:

🛒 1. Узнайте цену тарифа в звездах, она указана выше
👤 2. Перейдите в профиль @{PAYMENT_SETTINGS['support_username']}
📩 3. Отправьте подарок по стоимости тарифа
✅ 4. Отправьте скриншот оплаты в бота

Не обязательно предупреждать перед оплатой, всё просто, оплатили и получили тариф!

Инструкция : {PAYMENT_SETTINGS['stars_instruction']}"""

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("✅ Я оплатил", callback_data=f'paid_{index}_stars')
    btn2 = types.InlineKeyboardButton("✖️ Отменить", callback_data='show_categories')
    markup.add(btn1, btn2)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=markup
    )
    
    # Уведомление админам о запросе оплаты
    notify_admins(
        "⭐️ Запрос на оплату Stars", 
        call.from_user,
        f"Тариф: {tariff['name']}\nСумма: {tariff['price_stars']}⭐️"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('paid_'))
def paid(call):
    parts = call.data.split('_')
    index = int(parts[1])
    method = parts[2]
    
    text = """💰 Оплатили?

Отправьте боту квитанцию об оплате: скриншот или фото.
На квитанции должны быть четко видны: дата, время и сумма платежа.
Или вы можете отправить точную дату и время платежа"""

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_back = types.InlineKeyboardButton("🔙 Назад", callback_data=f'view_{index}')
    btn_cancel = types.InlineKeyboardButton("✖️ Отменить", callback_data='show_categories')
    markup.add(btn_back, btn_cancel)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=markup
    )
    
    # Сохраняем состояние ожидания квитанции
    user_states[call.from_user.id] = {
        "tariff_index": index,
        "payment_method": method,
        "waiting_receipt": True
    }

@bot.message_handler(content_types=['text', 'photo'])
def handle_receipt(message):
    user_id = message.from_user.id
    
    # Проверяем, ожидает ли пользователь отправки квитанции
    if user_id in user_states and user_states[user_id].get("waiting_receipt"):
        state = user_states[user_id]
        tariff = tariffs_data[state["tariff_index"]]
        method_map = {
            "card": "картой РФ",
            "ukr_card": "картой УКР",  # Добавлен новый метод
            "crypto": "криптовалютой",
            "cryptobot": "CryptoBot",
            "stars": "Stars"
        }
        method = method_map.get(state["payment_method"], state["payment_method"])
        
        # Определяем сумму в зависимости от метода оплаты
        if state["payment_method"] == "card":
            amount = tariff['price_rub']
        elif state["payment_method"] == "ukr_card":
            amount = tariff['price_uah']
        elif state["payment_method"] in ["crypto", "cryptobot"]:
            amount = tariff['price_usd']
        else:  # stars
            amount = tariff['price_stars']
        
        # Сохраняем квитанцию в БД
        if message.content_type == 'photo':
            add_receipt(
                user_id, 
                tariff['name'], 
                method, 
                amount,
                message.caption,
                message.photo[-1].file_id
            )
            
            # Уведомление админам с фото
            caption = f"📸 Получена квитанция (фото)\n\n👤 Пользователь: {message.from_user.first_name} (@{message.from_user.username}) ID: {user_id}\nТариф: {tariff['name']}\nСпособ оплаты: {method}\nСумма: {amount}"
            notify_admins_photo(message.from_user, message.photo[-1].file_id, caption)
        else:
            add_receipt(
                user_id, 
                tariff['name'], 
                method, 
                amount,
                message.text
            )
            
            # Уведомление админам с текстом
            notify_admins(
                "📝 Получена квитанция (текст)", 
                message.from_user,
                f"Тариф: {tariff['name']}\nСпособ оплаты: {method}\nСумма: {amount}\n\nТекст: {message.text}"
            )
        
        # Ответ пользователю
        bot.reply_to(message, "✅ Спасибо! Квитанция отправлена на проверку, вы получите уведомление как только её проверят.")
        
        # Возвращаем в главное меню
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("🦋 Тарuфы 🦋")
        btn2 = types.KeyboardButton("🦋 Моя подnuска 🦋")
        btn3 = types.KeyboardButton("🦋 Доказательства 🦋")
        btn4 = types.KeyboardButton("🦋 Тех.поддержка 🦋")
        markup.add(btn1, btn2, btn3, btn4)
        
        bot.send_message(
            message.chat.id,
            "Выберите действие:",
            reply_markup=markup
        )
        
        # Очищаем состояние
        del user_states[user_id]

bot.polling()
