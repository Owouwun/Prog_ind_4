#!/usr/bin/env python
import xml.etree.ElementTree as ET
import sqlite3

con = sqlite3.connect('chemistry.db')
cursor = con.cursor()

root = ET.Element('data')

cursor.execute("""select * from chemicals;""")
rows = cursor.fetchall()
for row in rows:
    chem = ET.Element('chemical')

    id = ET.Element('id')
    id.text = str(row[0])
    chem.append(id)

    name = ET.Element('name')
    name.text = str(row[1])
    chem.append(name)

    Class = ET.Element('class')
    Class.text = str(row[2])
    chem.append(Class)

    color = ET.Element('color')
    color.text = str(row[3])
    chem.append(color)

    root.append(chem)

cursor.execute("""select * from classes""")
rows = cursor.fetchall()
for row in rows:
    Class = ET.Element('class')

    id = ET.Element('id')
    id.text = str(row[0])
    Class.append(id)

    name = ET.Element('name')
    name.text = str(row[1])
    Class.append(name)

    org = ET.Element('organic')
    org.text = str(row[2])
    Class.append(org)

    root.append(Class)

cursor.execute("""select * from colors""")
rows = cursor.fetchall()
for row in rows:
    color = ET.Element('color')

    id = ET.Element('id')
    id.text = str(row[0])
    color.append(id)

    name = ET.Element('name')
    name.text = str(row[1])
    color.append(name)

    root.append(color)

tree = ET.ElementTree(root)
con.close()
tree.write('chemistries.xml')
print("Content-type: text/html\n")
print("""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Title</title>
    </head>
    <body>
            
    <h1>XML-файл успешно создан</h1>
    <form action= "main.py">
        <button type="submit">Вернуться на главную</button>
    </form>
""")