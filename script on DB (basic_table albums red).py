import sqlite3

con = sqlite3.connect('mp3_base.db')
cur = con.cursor()

#----------filter on basic_lib
cur.execute('SELECT * FROM basic_lib')
fetch = cur.fetchall()

a = 0
b = 0

try:
    while True:

        if '/' in fetch[a][5]:
            listok = ''
            rep_art = str(fetch[a][5]).replace('/', listok + 'others songs').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif len(fetch[a][5]) >= 43:
            rep_art = str(fetch[a][5]).replace(str(fetch[a][5]), 'others songs')
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif 'disc 2' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace('disk 2', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif '[special edition]' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace('[special edition]', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif ' (international version)' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace(' (international version)', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
        elif ', volume one' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace(', volume one', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
        elif '(european edition)' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace('(european edition)', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif '(tour edition)' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace('(tour edition)', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)

        elif '(unabridged)' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace('(unabridged)', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif ': part two' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace(': part two', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif ', pt. 2' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace(', pt. 2', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif 'live at ' in fetch[a][5]:
            rep_art = 'lives'
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif 'live in ' in fetch[a][5]:
            rep_art = 'lives'
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif ', part 2' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace(', part 2', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif 'singles' in fetch[a][5]:
            rep_art = 'others songs'
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif '(light album)' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace('(light album)', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif '[explicit]' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace('[explicit]', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif '(deluxe edition)' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace('(deluxe edition)', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif '(re-mastered)' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace('(re-mastered)', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif '(special edition)' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace('(special edition)', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif '(deluxe version)' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace('(deluxe version)', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif '(limited edition)' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace('(limited edition)', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif '(bonus track version)' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace('(bonus track version)', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        elif '(deluxe)' in fetch[a][5]:
            rep_art = str(fetch[a][5]).replace('(deluxe)', '').rstrip()
            con.cursor()
            cur.execute("UPDATE basic_lib set album =:album WHERE audio_id=:audio_id",
                        {"album": rep_art, "audio_id": fetch[a][1]})
            con.commit()
            b += 1
            print(b)
        else:
            pass
        a += 1
except:
    print('except script4base')
