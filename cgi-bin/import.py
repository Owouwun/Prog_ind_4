#!/usr/bin/env python
import xml.etree.ElementTree as ET
import sqlite3
import cgi
import main

con = sqlite3.connect("chemistry.db")
cur = con.cursor()

cur.execute("""DROP TABLE IF EXISTS chemicals;""")
cur.execute("""DROP TABLE IF EXISTS classes;""")
cur.execute("""DROP TABLE IF EXISTS colors;""")
con.commit()
main.createDB()

print("Content-type: text/html\n")
print("""<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Title</title>
        </head>
        <body>
            """)

root = ET.parse('chemistries.xml').getroot()
print(root.items)
for child in root:
    print()
    if child.tag == "color":
        #print(child.get("id"), child.get("name"))
        cur.execute("""insert into colors (id, name) values ('{0}', '{1}')""".format(
            child[0].text, child[1].text
        ))
    elif child.tag == "class":
        #print(child.get("id"), child.get("name"))
        cur.execute("""insert into classes (id, name, organic) values ('{0}', '{1}', '{2}')""".format(
            child[0].text, child[1].text, child[2].text
        ))
    elif child.tag == "chemical":
        #print(child.get("id"), child.get("name"), child.get("class"), child.get("color"))
        cur.execute("""insert into chemicals (id, name, class, color) values ('{0}', '{1}', '{2}', '{3}')""".format(
            child[0].text, child[1].text, child[2].text, child[3].text
        ))
        #Chem.Class = Classes.objects.get(id=child.get("Class"))
        #Chem.Color = Colors.objects.get(id=child.get("Color"))

con.commit()
con.close()
print("<h1>Данные успешно добавлены</h1>")
print("""<div">
    <form action= "main.py">
        <button type="submit">Вернуться на главную</button>
    </form>
    </div>""")

