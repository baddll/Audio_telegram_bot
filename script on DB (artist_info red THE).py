import sqlite3

con = sqlite3.connect('mp3_base.db')
cur = con.cursor()

#-----------------------del THE on artist table
a = 0
b = 0

cur.execute('SELECT * FROM artist_info')

fetch = cur.fetchall()
while a <= 100000000:

    if 'the ' in str(fetch[a][0]):
        rep_art = str(fetch[a][0]).replace('the ', '').lstrip()
        con.cursor()
        cur.execute("UPDATE artist_info set artist =:artist WHERE url=:url",
                    {"artist": rep_art, "url": fetch[a][1]})
        con.commit()
        b += 1
        print(b)
    a += 1
#-----


a = 0
b = 0

cur.execute('SELECT * FROM basic_lib')

fetch = cur.fetchall()
while True:

    if 'bring me the horizon' in str(fetch[a][4]):
        pass
    else:
        if 'the ' in str(fetch[a][4]):
            print(fetch[a][4])
            rep_art = str(fetch[a][4]).replace('the ', '')
            con.cursor()
            cur.execute("UPDATE basic_lib set artist =:artist WHERE audio_id=:audio_id",
                        {"artist": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
    a += 1