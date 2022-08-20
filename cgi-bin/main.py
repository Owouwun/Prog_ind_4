#!/usr/bin/env python
import cgi
import sqlite3


def getTable2(tableName, tableParam, *columns):
    con = sqlite3.connect('chemistry.db')
    cursor = con.cursor()

    cursor.execute("select * from " + tableName)
    record = cursor.fetchall()
    strings = [list(x) for x in record]

    html = ""
    html += "<table " + tableParam + ">"
    html += "<caption>" + tableName + "</caption>"
    html += "<tr>"
    for i in columns:
        html += "<th>" + str(i) + "</th>"
    html += "<th>delete</th>"
    html += "</tr>"
    for i in strings:
        html += "<tr>"
        for j in i:
            html += "<td>" + str(j) + "</td>"
        html += "<td><form action='main.py'><button name='del{0}' value='{1}'>-</button></form></td>".format(tableName, i[0])
        html += "</tr>"
    html += "</table>"
    return html


def deleter(tableName, id):
    try:
        con = sqlite3.connect('chemistry.db')
        cursor = con.cursor()
        cursor.execute("delete from {0} where id={1}".format(tableName, id))
        con.commit()
    except (Exception, sqlite3.Error) as error:
        print(error)
    finally:
        if con:
            cursor.close()
            con.close()


def addChemical():
    con = sqlite3.connect('chemistry.db')
    cursor = con.cursor()

    form = cgi.FieldStorage()
    cursor.execute("insert into chemicals (name, class, color) values ({0}, {1}, {2});".format("'"+form.getfirst("name", "nil")+"'",
                                                                                              form.getfirst("class", "nil"),
                                                                                              form.getfirst("color", "nil")))
    con.commit()

def createDB():
    try:
        con = sqlite3.connect('chemistry.db')

        create_table = '''CREATE TABLE IF NOT EXISTS colors (
                                        id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL UNIQUE ON CONFLICT REPLACE
                                        );'''
        cursor = con.cursor()
        cursor.execute(create_table)
        con.commit()

        create_table = '''CREATE TABLE IF NOT EXISTS classes (
                                            id INTEGER PRIMARY KEY,
                                            name TEXT NOT NULL UNIQUE ON CONFLICT REPLACE,
                                            organic INTEGER NOT NULL
                                            );'''
        cursor = con.cursor()
        cursor.execute(create_table)
        con.commit()

        create_table = '''CREATE TABLE IF NOT EXISTS chemicals (
                                                id INTEGER PRIMARY KEY,
                                                name TEXT NOT NULL UNIQUE ON CONFLICT REPLACE,
                                                class INTEGER NOT NULL,
                                                color INTEGER NOT NULL,
                                                FOREIGN KEY(class) REFERENCES classes(id),
                                                FOREIGN KEY(color) REFERENCES colors(id)
                                                );'''
        cursor = con.cursor()
        cursor.execute(create_table)
        con.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if con:
            con.close()


if __name__ == "__main__":
    print("Content-type: text/html\n")
    print("""<!DOCTYPE HTML>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Tables</title>
            </head>
            <body>""")

    form = cgi.FieldStorage()
    for i in ("chemicals", "classes", "colors"):
        if form.getfirst("del"+i):
            deleter(i, form.getfirst("del"+i))

    if form.getfirst("name"):
        addChemical()

    try:
        print(getTable2("chemicals", "border='1'", "id", "name", "class", "color"))
        print("<button><a href='/cgi-bin/add_chemical.py'>Add chemical</a></button>")
        print(getTable2("classes", "border='1'", "id", "name", "organic"))
        print("<button><a href='/add_class.html'>Add class</a></button>")
        print(getTable2("colors", "border='1'", "id", "name"))
        print("<button><a href='/add_color.html'>Add color</a></button>")
    except sqlite3.OperationalError:
        createDB()
        print("""No database has found. New database was created. Update the page.""")

    print("<br/><br/><button><a href='import.py'>Import DB from XML</a></button>")
    print("<br/><br/><button><a href='export.py'>Export DB to XML</a></button>")
    print("""</body>
            </html>""")
