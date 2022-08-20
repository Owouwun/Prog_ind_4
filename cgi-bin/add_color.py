#!/usr/bin/env python
import cgi
import sqlite3


form = cgi.FieldStorage()
name = form.getfirst("name", "nil")

con = sqlite3.connect('chemistry.db')
cursor = con.cursor()

cursor.execute("insert into colors (name) values ({0});".format("'" + name + "'"))
con.commit()

print("Content-type: text/html\n")
print("""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Success</title>
    </head>

    <body>
    <p>The color was successfully added!</p>
    <form action="/cgi-bin/main.py">
        <button>Return</button>
    </form>
    </body>
    </html>""")


