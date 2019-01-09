#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3
import telebot
from telebot import apihelper
import time
from telebot import types
from dbmodules import lib_insert
from dbmodules import toper
from dbmodules import for_send_from_top_func
from dbmodules import for_send_from_basic_func
from dbmodules import artists_inline_list
from dbmodules import for_send_from_album
from dbmodules import closer

token = 'token'
bot = telebot.TeleBot(token)
apihelper.proxy =  {'https': 'socks5://login:password@ip:port'}
API_KEY = 'lastfm_API_key'
users_dict = {}
album_dict = {}

@bot.message_handler(commands={'start', 'help'})
def start(message):
    try:
        
        if closer(message.chat.id) == None:#обращение к функции, которая закрывает доступ левым польщователям.
            #Для предоставления доступа необходимо в таблицу внести ID.
            pass
        else:
            con = sqlite3.connect('mp3_base.db')
            cur = con.cursor()
            cur.execute('SELECT * FROM users WHERE Id=:Id', {'Id': message.chat.id})
            
            #создание клавиатуры с командой /list
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
            callback_button = types.InlineKeyboardButton(text="/list")
            keyboard.add(callback_button)
            bot.send_message(message.chat.id, 'Чтобы увидеть весь список исполнителей, нажми на кнопку ниже:',
                             reply_markup=keyboard)#отправка сообщения после команды /start и открытие клавиатуры с кнопкой /list
    except:
        print('error 1: def start - basic_bot_file.')

@bot.message_handler(commands={None})#enter on keyboard
def sandler(message):

    if closer(message.chat.id) == None:
        pass
    else:
        con = sqlite3.connect('mp3_base.db')
        cur = con.cursor()

        cur.execute('SELECT * FROM basic_lib WHERE artist=:artist',{'artist': message.text})

        if cur.fetchone() == None:
            bot.send_message(message.chat.id, 'Артист отсутствует в базе')
        else:
            cur.execute('DELETE FROM for_send WHERE id=:id', {'id': message.chat.id}), con.commit()

            if '***' in message.text + '***group':
                btns = []
                keyboarder = types.InlineKeyboardMarkup()
                btns.append(types.InlineKeyboardButton(text="Top songs", callback_data="top_songs"))
                btns.append(types.InlineKeyboardButton(text="All songs", callback_data="all_songs"))
                btns.append(types.InlineKeyboardButton(text="Albums", callback_data="from_albums"))
                keyboarder.add(*btns)
                bot.send_message(message.chat.id, message.text, reply_markup=keyboarder, parse_mode='Markdown')
                con.cursor(), cur.execute("UPDATE users set last_artist=:last_artist WHERE id=:id",
                            {"last_artist": message.text, 'id': message.chat.id}), con.commit()
                users_dict[message.chat.id] = {'artist': message.text, 'counter': 4}
            else:
                print('omg')

def groups_list(a, b):#inline group list
    
    #а - порядковый номер исполнителя с которого начинается построение списка
    #b - порядковый номер исполнителя в конце списка а + 32
    
    d = 0

    keyboard = types.InlineKeyboardMarkup()
    btns = []

    try:
        while a <= b:
            btns.append(types.InlineKeyboardButton(text=str(artists_inline_list()[0][a]).title(),
                                                   callback_data=str(artists_inline_list()[1][a]).lower() + '***group'))
            a += 1
    except:
        #если в списке меньше 32 исполнителей, то срабатывает исключение и список будет доставлен пустыми блоками.
        c = b - artists_inline_list()[2]
        while d <= c:
            btns.append(types.InlineKeyboardButton(text=' ',
                                                   callback_data='ignore'))
            d += 1
        print('error 3: def group_list - basic_bot_file.')

    keyboard.add(*btns)
    return keyboard

def album_list(art):#albums list
    btns = []
    keyboard = types.InlineKeyboardMarkup()

    try:
        con = sqlite3.connect('mp3_base.db')
        cur = con.cursor()

        artist = art.lower()

        cur.execute('SELECT * FROM basic_lib WHERE artist=:artist', {'artist': artist})
        fetch_arto = cur.fetchall()
        lister = []
        a = 0

        while a <= len(fetch_arto) - 1:
            if fetch_arto[a][5] in lister:
                pass
            else:
                if len(str(fetch_arto[a][5])) >= 43:
                    pass
                else:
                    album = str(fetch_arto[a][5])
                    cur.execute('SELECT * FROM basic_lib WHERE artist=:artist AND album=:album',
                                {'artist': artist, 'album': album})
                    fetch = cur.fetchall()

                    if len(fetch) <=4:
                        pass
                    else:
                        btns.append(types.InlineKeyboardButton(text=str(fetch_arto[a][5]).title(),
                                                               callback_data=str((fetch_arto[a][5]) + '&&&album').lower()))
                        lister.append(fetch_arto[a][5])
            a = a + 1
        if lister == []:
            keyboard = 'to small songs'
        else:
            btns.append(types.InlineKeyboardButton(text='Back', callback_data='+back'))
            keyboard.add(*btns)
    except:
        print('error 4: def album_list - basic_bot_file.')
    return keyboard

@bot.message_handler(commands={'list'})#group list + remote buttons
def list(message):

    if closer(message.chat.id) == None:
        pass
    else:
        users_dict[message.chat.id] = 0
        con = sqlite3.connect('mp3_base.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM artist_info')

        btns = []

        if len(cur.fetchall()) <= 32:
            pass
        else:
            btns.append(types.InlineKeyboardButton(text="next", callback_data="next"))
        keyboard = groups_list(0, 32)
        keyboard.add(*btns)
        bot.send_message(message.chat.id, "Список исполнителей: ", reply_markup=keyboard, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'next')#inline for next-button
def callback_inline_next(call):
    ID = call.message.chat.id
    saver = users_dict.get(ID)
    dict_count = 0

    if (saver is not None):
        dict_count = saver
        dict_count += 32
    c = dict_count
    d = c + 32
    users_dict[ID] = c

    btns = []
    btns1 = []

    keyboard = groups_list(c, d)

    try:
        if c > 0:
            if d >= artists_inline_list()[2]:
                pass
            else:
                btns1.append(types.InlineKeyboardButton(text="next", callback_data="next"))
                keyboard.add(*btns1)
        if c < d:
            btns.append(types.InlineKeyboardButton(text="back", callback_data="back"))
            keyboard.add(*btns)
        bot.edit_message_text("Список исполнителей: ", call.from_user.id, call.message.message_id,
                              reply_markup=keyboard)
    except:
        print('error 5: def callback_inline - basic_bot_file.')

@bot.callback_query_handler(func=lambda call: call.data == 'back')#inline for back-button
def callback_inline_back(call):
    ID = call.message.chat.id

    saver = users_dict.get(ID)
    dict_count = 0

    if (saver is not None):
        dict_count = saver
        dict_count -= 32
    c = dict_count
    d = c + 32
    users_dict[ID] = c

    btns = []
    btns1 = []

    keyboard = groups_list(c, d)

    try:
        if c < d:
            btns1.append(types.InlineKeyboardButton(text="next", callback_data="next"))
            keyboard.add(*btns1)
        if c > 0:
            if d >= artists_inline_list()[2]:
                pass
            else:
                btns.append(types.InlineKeyboardButton(text="back", callback_data="back"))
                keyboard.add(*btns)
        bot.edit_message_text("Список исполнителей: ", call.from_user.id, call.message.message_id,
                              reply_markup=keyboard)
    except:
        print('error 6: def callback_inline_back - basic_bot_file.')

@bot.callback_query_handler(func=lambda mes: True)#обработчик всех команд + выбор альбома
def callback_inline(mes):
    if closer(mes.message.chat.id) == None:
        pass
    else:

        id = mes.message.chat.id
        album_dict = {}

        con = sqlite3.connect('mp3_base.db')
        cur = con.cursor()

        bot.edit_message_text(chat_id=mes.message.chat.id, message_id=mes.message.message_id, text=mes.data)
        keyboard1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
        keyboard2 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
        callback_button1 = types.InlineKeyboardButton(text="/next")
        callback_button2 = types.InlineKeyboardButton(text="/list")

        if '^^^' in mes.data:
            keyboard1.add(callback_button2)
            bot.send_message(mes.message.chat.id, 'genres', reply_markup=keyboard2)
        elif '&&&' in mes.data:
            try:
                cur.execute('DELETE FROM for_send WHERE id=:id', {'id': id}), con.commit()

                x = mes.data.split('&&&')
                a = 0
                c = (users_dict.get(id)['artist']).lower().split('***')[0]

                album_dict[id] = {x[0]}
                cur.execute('SELECT * FROM basic_lib WHERE artist=:artist AND album=:album',
                            {'artist': c, 'album': x[0]})
                fetch_artist = cur.fetchall()

                while a <= 4:
                    bot.send_audio(mes.message.chat.id, audio=fetch_artist[a][1])
                    a = a + 1
                else:
                    for_send_from_album(c, x[0], id)
                    keyboard1.add(callback_button2, callback_button1)
                    bot.send_message(mes.message.chat.id, '/next',
                                     reply_markup=keyboard1)
            except:
                keyboard1.add(callback_button2)
                bot.send_message(mes.message.chat.id, 'Выбери:',
                                 reply_markup=keyboard1)
                print('error 7: def callback_inline - basic_bot_file.')
        elif '***' in mes.data:
            bot.delete_message(mes.message.chat.id, mes.message.message_id)
            con.cursor()
            cur.execute("UPDATE users set last_artist=:last_artist WHERE id=:id", {"last_artist": mes.data.split('***')[0], 'id': id})
            con.commit()

            btns = []
            keyboarder = types.InlineKeyboardMarkup()
            btns.append(types.InlineKeyboardButton(text="Top songs", callback_data="top_songs"))
            btns.append(types.InlineKeyboardButton(text="All songs", callback_data="all_songs"))
            btns.append(types.InlineKeyboardButton(text="Albums", callback_data="from_albums"))
            btns.append(types.InlineKeyboardButton(text="Back", callback_data="-back"))
            keyboarder.add(*btns)
            bot.send_message(mes.message.chat.id, 'Choose:', reply_markup=keyboarder, parse_mode='Markdown')
            users_dict[id] = {'artist': mes.data, 'counter': 4}

        elif 'top_songs' == mes.data:
            bot.delete_message(mes.message.chat.id, mes.message.message_id)
            cur.execute('DELETE FROM for_send WHERE id=:id', {'id': id}), con.commit()

            try:
                keyboard1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
                callback_button1 = types.InlineKeyboardButton(text="/next")
                callback_button2 = types.InlineKeyboardButton(text="/list")

                under_split_artist = (users_dict.get(id)['artist']).lower()
                artist = under_split_artist.split('***')[0]

                toper(artist)

                c = 0
                d = 0

                try:
                    cur.execute('SELECT * FROM top_art_table WHERE artist=:artist', {'artist': artist})
                    fetch_art_top = cur.fetchall()
                    print('fetch art table')

                    while c <= 50:
                        if d == 5:
                            keyboard1.add(callback_button2, callback_button1)#, callback_button3)
                            bot.send_message(mes.message.chat.id, 'Чтобы открыть список групп, нажми на кнопку /list:',
                                             reply_markup=keyboard1)
                            break
                        if fetch_art_top[c][2] == None:
                            pass
                        else:
                            bot.send_audio(mes.message.chat.id, audio=fetch_art_top[c][2])
                            d = d + 1
                        c = c + 1
                    if len(fetch_art_top) >= 4:
                        for_send_from_top_func(artist, id)
                except:
                    print('error 7: send from top. 2st send')
            except:
                bot.send_message(mes.message.chat.id, 'Что-то пошло не так. Попробуй еще раз.')
                print('error 9: def top - basic_bot_file.')
        elif 'all_songs' == mes.data:

            bot.delete_message(mes.message.chat.id, mes.message.message_id)
            cur.execute('DELETE FROM for_send WHERE id=:id', {'id': id}), con.commit()

            try:
                keyboard1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
                callback_button1 = types.InlineKeyboardButton(text="/next")
                callback_button2 = types.InlineKeyboardButton(text="/list")

                keyboard2 = types.InlineKeyboardMarkup()
                btns = []
                btns.append(types.InlineKeyboardButton(text="Next", callback_data="-next"))
                keyboard2.add(*btns)

                under_split_artist = (users_dict.get(id)['artist']).lower()
                artist = under_split_artist.split('***')[0]

                a = 0
                b = 0

                try:
                    cur.execute("SELECT count(*) as total from basic_lib WHERE artist=:artist", {'artist': artist})
                    len_art = cur.fetchall()[0][0]
                    cur.execute('SELECT * FROM basic_lib WHERE artist=:artist', {'artist': artist})
                    fetch_artist = cur.fetchall()

                    try:
                        while a <= len_art:
                            if b == 5:
                                break
                            if fetch_artist[a][1] == None:
                                pass
                            else:
                                bot.send_audio(mes.message.chat.id, audio=fetch_artist[a][1])
                                b = b + 1
                            a = a + 1
                        bot.send_message(mes.message.chat.id, "Формируется список отправки, плз подождите")
                    except:
                        print('all songs except')

                    if len_art >= 6:
                        for_send_from_basic_func(artist, id)
                        keyboard1.add(callback_button2, callback_button1)
                        bot.send_message(mes.message.chat.id, 'Выбери:', reply_markup=keyboard1)
                    else:
                        print('pass all tracks')
                except:
                    print('error 8: def all - basic_bot_file.')
            except:
                bot.send_message(mes.message.chat.id, 'Что-то пошло не так. Попробуй еще раз.')
                print('error basic bot: command all')

        elif 'from_albums' == mes.data:
            bot.delete_message(mes.message.chat.id, mes.message.message_id)
            cur = con.cursor()
            cur.execute('DELETE FROM for_send WHERE id=:id', {'id': id}), con.commit()

            keyboard3 = types.InlineKeyboardMarkup()
            btns = []
            btns.append(types.InlineKeyboardButton(text="Back", callback_data="-back"))
            keyboard3.add(*btns)

            x = users_dict.get(id)['artist'].split('***')[0]

            if '/' in x:
                x = x.replace('/', '.')
            else:
                pass
            if album_list(x) == 'to small songs':
                print('sucks')
                bot.send_message(mes.message.chat.id, 'Слишком мало композиций данной группы.',reply_markup=keyboard3, parse_mode='Markdown')
            else:
                bot.send_message(mes.message.chat.id, 'Альбомы', reply_markup=album_list(x))

        elif "+back" == mes.data:
            bot.delete_message(mes.message.chat.id, mes.message.message_id)
            btns = []
            keyboarder = types.InlineKeyboardMarkup()
            btns.append(types.InlineKeyboardButton(text="Top songs", callback_data="top_songs"))
            btns.append(types.InlineKeyboardButton(text="All songs", callback_data="all_songs"))
            btns.append(types.InlineKeyboardButton(text="Albums", callback_data="from_albums"))
            btns.append(types.InlineKeyboardButton(text="Back", callback_data="-back"))
            keyboarder.add(*btns)
            bot.send_message(mes.message.chat.id, 'Choose:', reply_markup=keyboarder, parse_mode='Markdown')

            con.cursor()
            cur.execute("SELECT * FROM users WHERE id=:id", {"id": id})
            Xxx = cur.fetchone()
            users_dict[id] = {'artist': Xxx[2], 'counter': 4}

        elif "-back" == mes.data:
            bot.delete_message(mes.message.chat.id, mes.message.message_id)
            users_dict[mes.message.chat.id] = 0

            con = sqlite3.connect('mp3_base.db')
            cur = con.cursor()
            cur.execute('SELECT * FROM artist_info')
            x = len(cur.fetchall())
            btns = []

            if x <= 32:
                pass
            else:
                btns.append(types.InlineKeyboardButton(text="next", callback_data="next"))
            keyboard = groups_list(0, 32)
            keyboard.add(*btns)
            bot.send_message(mes.message.chat.id, "Список исполнителей: ", reply_markup=keyboard, parse_mode='Markdown')
        else:
            pass

@bot.message_handler(commands=['next'])#buttons for next 5 songs from for_send table
def nexter(message):
    try:
        keyboard1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
        callback_button2 = types.InlineKeyboardButton(text="/list")

        id = message.chat.id
        con = sqlite3.connect('mp3_base.db')
        cur = con.cursor()

        art = users_dict.get(id)['artist']
        saver = int(users_dict.get(id)['counter'])

        dict_count = 0
        if (saver is not None):
            dict_count = saver
            dict_count += 10
        c = dict_count
        users_dict[id] = {'artist': art, 'counter': c}

        A = c
        B = A - 9

        try:
            cur.execute('SELECT * FROM for_send WHERE id=:id', {'id': id})
            show_table = cur.fetchall()
            while B <= A:
                video_sender = show_table[B][1]
                bot.send_audio(message.chat.id, audio=video_sender)
                B += 1
            bot.send_message(message.chat.id, text='/next')
            print(B)
        except:
            keyboard1.add(callback_button2)
            bot.send_message(message.chat.id, '/list:', reply_markup=keyboard1)
            print('error 10: def nexter - basic_bot_file.')
    except:
        bot.send_message(message.chat.id, text='Что-то пошло не так. Попробуй еще раз.')

@bot.message_handler(content_types=['audio'])
def audio(message):#Добавление треков в БД
    if closer(message.chat.id) == None:
        pass
    else:
        try:
            id_user = message.chat.id
            format = message.audio.mime_type
            artist = message.audio.performer
            track = message.audio.title
            audio_id = message.audio.file_id
            duration = message.audio.duration

            if format.split('/')[1] == 'flac':
                pass
            else:
                lib_insert(id_user, format, artist, track, audio_id, duration)
        except:
            print('error 11: def audio - basic_bot_file.')

while True:
    try:
        bot.polling(none_stop=True, timeout=3.5)
    except:
        print('restart')
        time.sleep(10)
