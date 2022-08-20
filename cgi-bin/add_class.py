#!/usr/bin/env python
import cgi
import sqlite3


form = cgi.FieldStorage()
name = form.getfirst("name", "nil")
org = form.getfirst("organic", "nil")
if name != "nil":
    try:
        con = sqlite3.connect('chemistry.db')
        cursor = con.cursor()

        cursor.execute("insert into classes (name, organic) values ({0}, {1});".format("'" + name + "'", "'" + org + "'"))
        con.commit()
    except (Exception, sqlite3.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if con:
            cursor.close()
            con.close()
print("Content-type: text/html\n")
print("""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Success</title>
    </head>

    <body>
    <p>The class was successfully added!</p>
    <form action="/cgi-bin/main.py">
        <button>Return</button>
    </form>
    </body>
    </html>""")