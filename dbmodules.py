#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3
import requests
import random
import time
from datetime import datetime
API_KEY = 'lastfm_key'

#данная функция запрашивает у сайта lastfm информацию о песне и добавляет в таблицу basic_lib в месте с идентификатором песни
def lib_insert(id_user, format, artist, track, audio_id, duration):

    con = sqlite3.connect('mp3_base.db')
    cur = con.cursor()

    try:
        artist_perem = artist.lower()
        track_perem = track.lower()

        tag0 = None
        tag1 = None
        tag2 = None
        tag3 = None
        tag4 = None

        date = datetime.strftime(datetime.now(), "%d.%m.%Y")
        timer = str(datetime.strftime(datetime.now(), "%H:%M:%S.%f"))

        con.cursor(), cur.execute('SELECT * FROM users_lib WHERE audio_id=:audio_id', {'audio_id': audio_id})
        fetch_users_lib = cur.fetchone()
        users_songs = ((id_user, audio_id, duration, format, artist_perem, track_perem, date + ' ' + timer),)

        if fetch_users_lib == None:
            print('insert in users lib')
            cur.executemany(
                "INSERT INTO users_lib VALUES(?, ?, ?, ? , ?, ?, ?)", users_songs), con.commit()

        con.cursor(), cur.execute('SELECT * FROM basic_lib WHERE audio_id=:audio_id', {'audio_id': audio_id})
        fetch_audio = cur.fetchone()

        if fetch_audio == None:

            try:
                artist_info(artist_perem)
                one_artist_song_len(artist_perem)
            except:
                print('dbmodules, def lib_insert, error 1: dont insert artist info')

            res = requests.get(
                "http://ws.audioscrobbler.com/2.0/?", params={'method': 'track.getInfo',
                                                              "api_key": API_KEY,
                                                              "artist": artist_perem,
                                                              "track": track_perem,
                                                              "format": "json"})
            data = res.json()
            #------Artist, album, track
            try:
                album_req = str((data['track']['album']['title']).lower())

                try:
                    tag0 = data['track']['toptags']['tag'][0]['name']
                    tag1 = data['track']['toptags']['tag'][1]['name']
                    tag2 = data['track']['toptags']['tag'][2]['name']
                    tag3 = data['track']['toptags']['tag'][3]['name']
                    tag4 = data['track']['toptags']['tag'][4]['name']
                except:
                    print('dbmodules, def lib_insert, error 2: dbmodule - failed insert tag or tags')
                #-----------------------------

                song_info = ((id_user, audio_id , duration, format, artist_perem, album_req, track_perem, tag0, tag1, tag2, tag3, tag4, date + ' ' + timer),)

                try:
                    cur.execute('SELECT * FROM basic_lib WHERE artist=:artist AND track=:track',
                                {'artist': artist_perem, 'track': track_perem})
                    fetch_audi = cur.fetchone()

                    if fetch_audi == None:
                        print('fetch audi NONE')
                        print(timer + ' ' + artist_perem + ' ' + track_perem + ' INSERT to base')
                        cur = con.cursor()
                        cur.executemany(
                            "INSERT INTO basic_lib VALUES(?, ?, ?, ? , ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            song_info)
                        con.commit()
                        con.close()

                    else:
                        if fetch_audi[2] < duration:
                            print(artist_perem + '  ' + track_perem)
                            updater(artist_perem, track_perem)

                            time.sleep(1)

                            print(timer + ' ' + artist_perem + ' ' + track_perem + ' update to base')
                            cur = con.cursor()
                            cur.executemany(
                                "INSERT INTO basic_lib VALUES(?, ?, ?, ? , ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                song_info)
                            con.commit()
                            con.close()

                    ran = random.uniform(0.1, 0.5)
                    time.sleep(ran)
                except:
                    print('dbmodules, def lib_insert, error 3: error insert to base')
            except:
                print('dbmodules, def lib_insert, error 4: dbmodule - none artist, alb or track')
    except:
        print('dbmodules, def lib_insert, error 5: audio nuances')

#Данная функция запрашивает у сайта lastfm информацию об исполнителе и добавляет в таблицу
def artist_info(artist):
    con = sqlite3.connect('mp3_base.db')
    cur = con.cursor()

    try:
        res = requests.get(
            "http://ws.audioscrobbler.com/2.0/?", params={'method': 'artist.getinfo',
                                                          "artist": artist,
                                                          "api_key": API_KEY,
                                                          "autocorrect": 1,
                                                          "format": "json"})
        data = res.json()

        con.cursor()
        cur.execute('SELECT * FROM artist_info WHERE artist=:artist', {'artist': data['artist']['name'].lower()})
        fetch_artist = cur.fetchone()
        print('artist info in artist info' + str(fetch_artist))

        if fetch_artist == None:

            name = data['artist']['name']
            url = data['artist']['url']
            tag0 = data['artist']['tags']['tag'][0]['name']
            tag1 = data['artist']['tags']['tag'][1]['name']
            tag2 = data['artist']['tags']['tag'][2]['name']
            tag3 = data['artist']['tags']['tag'][3]['name']
            tag4 = data['artist']['tags']['tag'][4]['name']
            len_art = 0

            artist_db = ((name.lower(), url, tag0, tag1, tag2, tag3, tag4, len_art),)
            print(artist_db)
            print('insert in artist_info')
            con.cursor()
            cur.executemany(
                "INSERT INTO artist_info VALUES(?, ?, ?, ? , ?, ?, ?, ?)", artist_db)
            con.commit()

            ran = random.uniform(0.1, 2.0)
            time.sleep(ran)
        else:
            print('dbmodules, def artist_info, error 1: dont insert in artist base')
    except:
        print('dbmodules, def artist_info, error 2: error insert artist')

#данная функция запрашивает у сайта lastfm топ 50 трэков исполнителя и вносит в таблицу top_art_table
#если в таблице имеется исполнитель то запрос к lastfm делаться не будет. Также данную таблицу можно периодически отчищать
#в случае если понравятся свежие топы.
#так же он проверяет наличие пропущенных треков в основной таблице, если они вдруг появились позднее.
def toper(artist):

    a = 0
    b = 0

    con = sqlite3.connect('mp3_base.db')
    cur = con.cursor()
    cur.execute("SELECT count(*) as total from top_art_table WHERE artist=:artist", {'artist': artist})
    fetch_audio = cur.fetchall()[0][0]

    if fetch_audio == 0:

        res = requests.get(
            "http://ws.audioscrobbler.com/2.0/?", params={'method': 'artist.gettoptracks',
                                                          "artist": artist,
                                                          "api_key": API_KEY,
                                                          "format": "json"})
        data = res.json()

        print('LAST FM module requested')

        try:
            while True:
                x = (data['toptracks']['track'][a]['name']).lower()
                art_info = ((artist, x, None),)
                cur.executemany("INSERT INTO top_art_table VALUES(?, ?, ?)", art_info)
                a = a + 1
        except:
            print('dbmodules, def toper, error 1: except on execute song id')
        con.commit()
    else:
        print('none')

    cur = con.cursor()
    cur.execute('SELECT * FROM basic_lib WHERE artist=:artist', {'artist': artist})
    show_file_id = cur.fetchall()#[1][1]

    try:
        while b <= len(show_file_id):
            cur = con.cursor()
            cur.execute("UPDATE top_art_table set file_id =:file_id where artist=:artist AND song=:song",
                                {"file_id": show_file_id[b][1], "artist": artist, 'song': show_file_id[b][6]})
            b = b + 1
    except:
        print('dbmodules, def toper, error 2: error update tracks on top')
    con.commit()
    con.close()

#данная функция ищет дубль песни и в случае если песня по длинне меньше залитой, то пропускает ее.
def updater(artist,track):

    con = sqlite3.connect('mp3_base.db')
    cur = con.cursor()

    print('updateclonemodule in work')

    try:
        print('del clone with bad duration')
        cur.execute('DELETE from basic_lib where artist=:artist AND track=:track',{'artist': artist, 'track': track})
        con.commit()
    except:
        print('dbmodules, def updater, error 1: except on update track on basic_lib ')
    con.close()

#эта функция обновляет колличество песен одного исполнителя
def one_artist_song_len(art):
    con = sqlite3.connect('mp3_base.db')
    cur = con.cursor()

    try:
        artist = art

        cur.execute('SELECT * FROM artist_info WHERE artist=:artist', {'artist': artist})
        fetch_artist = cur.fetchall()
        print(fetch_artist)

        con.cursor()
        cur.execute('SELECT * FROM basic_lib WHERE artist=:artist', {'artist': artist})
        fetch_arto = cur.fetchall()
        len_sg = len(fetch_arto)
        print(len_sg)

        if len_sg != fetch_artist:
            cur.execute("UPDATE artist_info set len_art =:len_art where artist=:artist",
                        {"len_art": len_sg, "artist": artist})
            con.commit()

            print('update songs in artist_info ended')
        else:
            pass
        con.close()
    except:
        print('dbmodules, def  one_artist_song_len, error 1: except on update len song on artist_info')

#данная функция отправляет все трэки без разбора из таблице basic_lib
def for_send_from_basic_func(art, id):
    con = sqlite3.connect('mp3_base.db')

    try:
        a = 0
        b = 0

        cur = con.cursor()
        cur.execute("SELECT count(*) as total from basic_lib WHERE artist=:artist", {'artist': art})
        len_art = cur.fetchall()[0][0]

        cur.execute('SELECT * FROM basic_lib WHERE artist=:artist', {'artist': art})
        fetch_artist = cur.fetchall()


        while a <= len_art:
            if b == 50:
                break
            if fetch_artist[a][1] == None:
                pass
            else:
                con.cursor()
                cur.execute("INSERT INTO for_send VALUES(?,?)", (id, fetch_artist[a][1]), )
                con.commit()
                b = b + 1
            a = a + 1
    except:
        print('dbmodules, def for_send_from_basic_func, error 1: from basic_lib table insert to for_send')
    con.close()

#данная команда отправляется все трэки по исполнителю из таблицы top_art_table
def for_send_from_top_func(art, id):
    con = sqlite3.connect('mp3_base.db')
    try:
        a = 0
        b = 0

        cur = con.cursor()
        cur.execute("SELECT count(*) as total from top_art_table WHERE artist=:artist", {'artist': art})
        len_art = cur.fetchall()[0][0]

        cur.execute('SELECT * FROM top_art_table WHERE artist=:artist', {'artist': art})
        fetch_artist = cur.fetchall()

        while a <= len_art:
            if b == 50:
                break
            if fetch_artist[a][2] == None:
                pass
            else:
                con.cursor()
                cur.execute("INSERT INTO for_send VALUES(?,?)", (id, fetch_artist[a][2]), )
                con.commit()
                b = b + 1
            a = a + 1
    except:
        print('dbmodules, def  for_send_from_top_func, error 1: from top_art_table insert to for_send')
    con.close()

#данная функция отправляет трэки из выбранного альбома исполнителя
def for_send_from_album(art, alb, id):
    con = sqlite3.connect('mp3_base.db')

    try:
        cur = con.cursor()
        cur.execute('SELECT * FROM basic_lib WHERE artist=:artist AND album=:album', {'artist': art, 'album': alb})
        fetch_album = cur.fetchall()

        a = 0

        while a <= len(fetch_album):
                con.cursor()
                cur.execute("INSERT INTO for_send VALUES(?,?)", (id, fetch_album[a][1]),)
                con.commit()
                a = a + 1
    except:
        print('dbmodules, def for_send_from_album, error 1: for send from album')

#данная функция выводит всех артистов в inline список в чате
def artists_inline_list():
    con = sqlite3.connect('mp3_base.db')

    cur = con.cursor()
    cur.execute('SELECT * FROM artist_info')
    fetch_artist = cur.fetchall()
    a = 0

    lis = []
    lis1 = []

    try:
        while True:
            if fetch_artist[a][7] <= 4:
                pass
            else:
                lis.append(str(fetch_artist[a][0]).capitalize() + ': ' + str(fetch_artist[a][7]))
                lis1.append(str(fetch_artist[a][0]).capitalize())
            a = a + 1
    except:
        pass
    return sorted(lis), sorted(lis1), len(lis)

#данная функция выводит список альбомов в inline по выбранному из inline клавиатуры исполнителей выше
def albums_inline_list(art):
    con = sqlite3.connect('mp3_base.db')
    cur = con.cursor()

    artist = art
    cur.execute('SELECT * FROM basic_lib WHERE artist=:artist', {'artist': artist})
    fetch_arto = cur.fetchall()
    lister = []
    a = 0
    try:
        while a <= len(fetch_arto) - 1:
            if fetch_arto[a][5] in lister:
                pass
            else:
                lister.append(fetch_arto[a][5])
            a = a + 1
    except:
        print('dbmodules, def albums_inline_list, error 1: except create buttons from artist albums')
    len_alb = len(lister)
    return lister, len_alb

def closer(ID): #функция разрешающая доступ к боту только для определенного количества пользователей

    con = sqlite3.connect('mp3_base.db')
    cur = con.cursor()
    con.cursor(), cur.execute('SELECT * FROM users WHERE Id=:Id', {'Id': ID})
    return cur.fetchone()
