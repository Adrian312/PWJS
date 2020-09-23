import sqlite3
import app

if __name__ == "__main__":

    conn = sqlite3.connect('database.db')
    print("BD otwarta")
    
    conn.execute('CREATE TABLE uzytkownik (id INTEGER PRIMARY KEY, imie TEXT, nazwisko TEXT, login TEXT, haslo TEXT)')
    conn.execute('CREATE TABLE post (operacja TEXT, sposob_wykonania TEXT, autor TEXT)')
    
    cur = conn.cursor()
    
    cur.execute("INSERT INTO uzytkownik (imie, nazwisko, login, haslo) VALUES (?,?,?,?)",('Adrian','Stolarz','adi','peugeot123') )
    conn.commit()
    
    cur.execute("SELECT id FROM uzytkownik WHERE login='adi'")
    row = cur.fetchall()
    for r in row:
        app.User(r[0])
    
    cur.execute("INSERT INTO post (operacja, sposob_wykonania, autor) VALUES (?,?,?)",('Wymiana oleju','Mechanicy i specjaliści radzą, aby w autach, które są przede wszystkim eksploatowane w mieście, wymieniać olej częściej, co 10 – 12 tys. km przebiegu. Zaleca się, aby w samochodach z instalacją gazową wymieniać olej co 10 tys. km przebiegu.','Adrian Stolarz') )
    conn.commit()

    cur.execute('SELECT * FROM uzytkownik ORDER BY imie')
    print(cur.fetchall())
    
    cur.execute('SELECT * FROM post')
    print(cur.fetchall())
    
    conn.close()
    print("BD zamknieta")