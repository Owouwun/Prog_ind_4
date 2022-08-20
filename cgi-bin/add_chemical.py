#!/usr/bin/env python
import sqlite3

if __name__ == "__main__":
    con = sqlite3.connect('chemistry.db')
    cursor = con.cursor()
    cursor.execute("select * from classes;")

    res = cursor.fetchall()
    #name[b][(m, n)]: b=0 - inorganic, b=1 - organic
    #               m = id
    #               n = name
    name = []
    for i in range(2):
        name.append([])
    for i in res:
        if not i[2]:
            name[0].append([i[0], i[1]])
        else:
            name[1].append([i[0], i[1]])

    print("""Content-type: text/html
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Add chemical</title>
        </head>
        <body>\n""")
    print("""
        <form action="/cgi-bin/main.py">
            <p>Chemical compound name:</p>
            <input type="text" name="name"><br/>
            
            <p>Class:</p>
            <select name="class" size="5">
                <optgroup label="Inorganic">""")
    for i in name[0]:
        print("""   <option value="{0}">{1}</option>""".format(i[0], i[1]))
    print("""   </optgroup>
                <optgroup label="Organic">""")
    for i in name[1]:
        print("""   <option value="{0}">{1}</option>""".format(i[0], i[1]))
    print("""   </optgroup>
            </select><br/>
            
            <p>Color:</p>
            <select name="color">""")
    cursor.execute("select * from colors;")
    res = cursor.fetchall()
    for i in res:
        print("""<option value="{0}">{1}</option>""".format(i[0], i[1]))
    print("""</select><br/><br/>
            <button>Add chemical</button>
            </form>

            </body>
            </html>""")
