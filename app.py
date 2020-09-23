from flask import Flask, Response, redirect, url_for, request, session, abort, render_template
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user
import sqlite3 as sql

app = Flask(__name__)

app.config.update(
 DEBUG = False,
 SECRET_KEY = 'sekretny_klucz'
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id):
        con = sql.connect('database.db')
        cur = con.cursor()
        self.id = id
        cur.execute("SELECT login, haslo FROM uzytkownik WHERE id = " + str(id))
        row = cur.fetchall()
        for r in row:
            self.name = str(r[0])
            self.password = str(r[1])

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

@app.route("/")
def main():
     dane = {'tytul': 'Witaj na stronie głównej Auto Land!', 'tresc': 'Czytaj, dodawaj, ucz się!'}
     return render_template('index.html', tytul = dane['tytul'], tresc = dane['tresc'])

@app.route("/dodajUzytkownika")
def dodaj():
    dane = {'tytul': 'Zarejestruj się!', 'tresc': 'Podaj dane!'}
    return render_template('rejestracja.html', tytul = dane['tytul'], tresc = dane['tresc'])

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            imie = request.form['imie']
            nazwisko = request.form['nazwisko']
            login = request.form['login']
            haslo = request.form['haslo']
            
            conn = sql.connect("database.db")
            cur = conn.cursor()
            cur.execute("SELECT COUNT(1) FROM uzytkownik WHERE login = '" + login + "'")
    
            if not cur.fetchone()[0]:
                cur.execute("INSERT INTO uzytkownik (imie, nazwisko, login, haslo) VALUES (?, ?, ?, ?)", (imie, nazwisko, login, haslo))
                conn.commit()
                msg = "Pomyslnie zarejestrowano użytkownika! Od teraz możesz przeglądać stronę!"
            else:
                msg = "Login jest zajęty!"
        except:
            conn.rollback()
            msg = "Podczas rejestracji wystąpił błąd!"
        finally:
            return render_template("wynik.html", tytul = "Rezultat", tresc = msg)
            conn.close()

@app.route("/listaUzytkownikow")
@login_required
def lista():
    dane = {'tytul': 'Lista użytkowników', 'tresc': 'Poniżej znajdują się zarejestrowane konta!'}
    con = sql.connect('database.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM uzytkownik order by imie")
    rekordy = cur.fetchall()
    con.close()
    return render_template('lista_uzytkownikow.html', tytul = dane['tytul'], tresc = dane['tresc'], rekordy = rekordy)

@app.route("/dodajPost")
@login_required
def dodajPost():
    dane = {'tytul': 'Witamy serdecznie!', 'tresc': 'Poniżej możesz podzielić się swoją wiedzą z innymi!'}
    return render_template('dodaj_post.html', tytul = dane['tytul'], tresc = dane['tresc'])

@app.route('/addrecc',methods = ['POST', 'GET'])
def addrecc():
    if request.method == 'POST':
        try:
            operacja = request.form['operacja']
            sposob_wykonania = request.form['sposob_wykonania']
            autor = request.form['autor']
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO post (operacja, sposob_wykonania, autor) VALUES (?,?,?)",(operacja,sposob_wykonania,autor))
                con.commit()
                msge = "Udało Ci się dodać poradnik!"
        except:
            con.rollback()
            msge = "Nie udało Ci się dodać poradniku!"
        finally:
            return render_template("wynik.html", tresc = msge)
            cur.close()
            con.close()
            
@app.route("/listaPostow")
@login_required
def listaPostow():
    con = sql.connect('database.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('SELECT * FROM post')
    rekordy = cur.fetchall()
    con.close()
    return render_template('lista_postow.html', rekordy = rekordy)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sql.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT COUNT(1) FROM uzytkownik WHERE login = '" + username +"'")

        if not cur.fetchone()[0]:
             return abort(401)
        else:
            cur.execute("SELECT id, haslo FROM uzytkownik WHERE login = '" + username +"'")
            row = cur.fetchall()
            for r in row:
                if password == r[1]:
                    user = User(r[0])
                    login_user(user)
                    return redirect(url_for("main"))
                else:
                    return abort(401)
    else:
        return render_template('logowanie.html')

#Procedura wylogowania    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    dane = {'tytul': 'Wylogowanie'}
    return render_template('wylogowanie.html', tytul = dane['tytul'])

#Procedura obsługi błędu logowania
@app.errorhandler(401)
def page_not_found(e):
    dane = {'tytul': 'Coś poszło nie tak...', 'blad': '401'}
    return render_template('blad.html', tytul = dane['tytul'], blad = dane['blad'])

#Przeładowanie uzytkownika
@login_manager.user_loader
def load_user(userid):
    return User(userid)

if __name__ == "__main__":
    app.run()