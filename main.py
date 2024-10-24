import time
import ITT
from telebot import types, telebot
from searcher import search
from postgresBD import *

bot = telebot.TeleBot("7742642039:AAE8GfyjQF6FdREDaMagvrJNHn-A44VYyPg")
users = {}
usersSettings = {}

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    id = str(call.message.chat.id)
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Настройки")
    markup.add(item1)
    if call.data == "registerYES":
        updateSession(call.message.chat.id, "register", "1")
        bot.send_message(call.message.chat.id, text="Настройки изменены")
    elif call.data == "registeNO":
        updateSession(call.message.chat.id, "register", "0")
        bot.send_message(call.message.chat.id, text="Настройки изменены")
    elif call.data in ["different0", "different1", "different2", "different3"]:
        updateSession(call.message.chat.id, "differentcharacters", call.data[9:len(call.data)])
        bot.send_message(call.message.chat.id, text="Настройки изменены")
    elif call.data == "register":
        keyboard = types.InlineKeyboardMarkup()
        registerButton = types.InlineKeyboardButton(text='Да', callback_data='registerYES')
        keyboard.add(registerButton)
        differentButton= types.InlineKeyboardButton(text='Нет', callback_data='registeNO')
        keyboard.add(differentButton)
        bot.send_message(call.message.chat.id, text="Учитывать регистр?", reply_markup=keyboard)
    elif call.data == "different":
        keyboard = types.InlineKeyboardMarkup()
        differentButton0 = types.InlineKeyboardButton(text='0', callback_data='different0')
        keyboard.add(differentButton0)
        differentButton1 = types.InlineKeyboardButton(text='1', callback_data='different1')
        keyboard.add(differentButton1)
        differentButton2 = types.InlineKeyboardButton(text='2', callback_data='different2')
        keyboard.add(differentButton2)
        differentButton3 = types.InlineKeyboardButton(text='3', callback_data='different3')
        keyboard.add(differentButton3)
        bot.send_message(call.message.chat.id, text="Сколько букв может отсутствовать в слове?", reply_markup=keyboard)
    elif call.data == "replaceYes" and users[id]["step"] == 2:
        users[id]["step"] += 1
        bot.send_message(call.message.chat.id,"Слово на замену", reply_markup=markup)
    elif call.data == "replaceNo" and users[id]["step"] == 2:
        users[id]["data"].append(None)
        result = search(text=users[id]["data"][0], word=users[id]["data"][1], register=(getSession(id)[0][2] == 1), replace=None, differentCharacters=getSession(id)[0][3])
        del users[id]
        result = "Ничего не найденно" if result == "" else result
        bot.send_message(call.message.chat.id, result, reply_markup=markup)


@bot.message_handler(content_types=['photo'])
def itt_messaeg(message):
    print("Dsaasdas")
    id = str(message.chat.id)
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    nameFile = f'images/{message.chat.id}_{time.time()}.jpg'
    with open(nameFile, 'wb') as new_file:
        new_file.write(downloaded_file)
        new_file.close()
    text = ITT.itt(nameFile)
    users[id] = {"data": [text], "step": 1}
    print(users)
    bot.send_message(chat_id=message.chat.id, text=text)
    bot.send_message(message.chat.id, f"Отправте слово которое нужно найти")



@bot.message_handler(content_types=['text'])
def text_message(message):
    
    if not exitsSession(message.chat.id):
        newSession(message.chat.id)
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Настройки")
    markup.add(item1)
    if message.text == "/start":
        bot.send_message(message.chat.id,"Привет ✌️. Я бот для поиска слов в предложениях. Если хотите найти в тексте слово. Просто отправте текст", reply_markup=markup)
    elif message.text == "Настройки":
        if message.chat.id in users:
            del users[message.chat.id]
        keyboard = types.InlineKeyboardMarkup()
        registerButton = types.InlineKeyboardButton(text='Настройик регистра', callback_data='register')
        keyboard.add(registerButton)
        differentButton= types.InlineKeyboardButton(text='Настройки несовпадения', callback_data='different')
        keyboard.add(differentButton)
        bot.send_message(message.chat.id,"Настройки бота", reply_markup=keyboard)
    else:
        id = str(message.chat.id)
        start = time.time()
        if id in users:
            if users[id]["step"] == 1:
                users[id]["step"] += 1
                users[id]["data"].append(message.text)
                keyboard = types.InlineKeyboardMarkup()
                key_yes = types.InlineKeyboardButton(text='Да', callback_data='replaceYes')
                keyboard.add(key_yes)
                key_no= types.InlineKeyboardButton(text='Нет', callback_data='replaceNo')
                keyboard.add(key_no)
                bot.send_message(message.chat.id, "Нужно ли заменить это слово?", reply_markup=keyboard)
            elif users[id]["step"] == 3:
                users[id]["step"] += 1
                users[id]["data"].append(message.text)
                result = search(users[id]["data"][0], users[id]["data"][1], getSession(id)[0][1], users[id]["data"][2], getSession(id)[0][2])
                del users[id]
                result = "Ничего не найденно" if result == "" else result
                bot.send_message(message.chat.id, text=result, reply_markup=markup)
        else:
            users[id] = {"data": [message.text], "step": 1}
            bot.send_message(message.chat.id,"Отправте слово которое нужно найти", reply_markup=markup)
        print(time.time()-start)


if __name__ == "__main__":
    print("Start bot")
    bot.polling(none_stop=True, interval=0)