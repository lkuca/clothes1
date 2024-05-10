from tkinter import Tk, ttk
import tkinter as tk
from sqlite3 import *
from sqlite3 import Error
from os import *

def create_connect(path:str):
    connection=None
    try:
        connection=connect(path)
        print("Ühendus on olemas!")
    except Error as e:
        print(f"Tekkis viga: {e}")
    return connection

def execute_query(connection,query):
    try:
        cursor=connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Tabel on loodud või andmed on sisestatud")
    except Error as e:
        print(f"Tekkis viga: {e}")

def execute_read_query(connection,query):
    cursor=connection.cursor()
    result=None
    try:
        cursor.execute(query)
        result=cursor.fetchall()
        return result
    except Error as e:
        print(f"Tekkis viga: {e}")

def tooted_query(connection, data):
    query = "INSERT INTO tooted(toote_nimi,hind,kategooria_id,brandi_id) VALUES(?,?,?,?)"
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()

def kategooriad_query(connection, kategooria_nimi):
    query = "INSERT INTO kategooriad(kategooria_nimi) VALUES(?)"
    cursor = connection.cursor()
    cursor.execute(query, (kategooria_nimi,))
    connection.commit()

def brandid_query(connection, brandi_nimi):
    query = "INSERT INTO brandid(brandi_nimi) VALUES(?)"
    cursor = connection.cursor()
    cursor.execute(query, (brandi_nimi,))
    connection.commit()

def Andmed(entry1, entry2, entry3, entry4):
    toote_nimi = entry1.get()
    hind = entry2.get()
    kategooria_nimi = entry3.get()
    brandi_nimi = entry4.get()

    tree.insert("", "end", values=(toote_nimi, hind, kategooria_nimi, brandi_nimi))

    tooted_query(conn, (toote_nimi, hind, kategooria_nimi, brandi_nimi))

 
    tree.delete(*tree.get_children())
    tooted = execute_read_query(conn, select_tooted)
    for row in tooted:
        tree.insert("", "end", values=row)

create_tooted_table = """
CREATE TABLE IF NOT EXISTS tooted(
toote_id INTEGER PRIMARY KEY AUTOINCREMENT,
toote_nimi TEXT NOT NULL,
hind INTEGER NOT NULL,
kategooria_id INTEGER,
brandi_id INTEGER,
FOREIGN KEY (kategooria_id) REFERENCES kategooriad(kategooria_id),
FOREIGN KEY (brandi_id) REFERENCES brandid(brandi_id)
)
"""

create_kategooriad_table = """
CREATE TABLE IF NOT EXISTS kategooriad(
kategooria_id INTEGER PRIMARY KEY AUTOINCREMENT,
kategooria_nimi TEXT NOT NULL
)
"""

create_brandid_table = """
CREATE TABLE IF NOT EXISTS brandid(
brandi_id INTEGER PRIMARY KEY AUTOINCREMENT,
brandi_nimi TEXT NOT NULL
)
"""

insert_tooted = """
INSERT INTO
tooted(toote_nimi, hind, kategooria_id, brandi_id)
VALUES
("t-särk", 20, 1, 1),
("tossud", 100, 2, 2)
"""

insert_kategooriad = """
INSERT INTO
kategooriad(kategooria_nimi)
VALUES
("t-särgid"),
("kingad")
"""

insert_brandid = """
INSERT INTO
brandid(brandi_nimi)
VALUES
("adidas"),
("nike")
"""

select_tooted = "SELECT * FROM tooted"
select_kategooriad = "SELECT * FROM kategooriad" 
select_brandid = "SELECT * FROM brandid"

filename = path.abspath(__file__)
dbdir = filename.rstrip('clothes1.py')
dbpath = path.join(dbdir,"data.db")
conn = create_connect(dbpath)


aken = Tk()
aken.geometry("1020x600")
aken.title("Clothes")

tree = ttk.Treeview(aken, column=("1", "2", "3", "4", "5"), show="headings")
tree.pack(expand=True, fill="both")

tree.heading("#1", text="ID")
tree.heading("#2", text="Toote_nimi")
tree.heading("#3", text="Hind")
tree.heading("#4", text="Kategooria_nimi")
tree.heading("#5", text="Brandi_nimi")

label1 = tk.Label(aken, text="Toote_nimi:")
label1.pack()

entry1 = tk.Entry(aken)
entry1.pack()

label2 = tk.Label(aken, text="Hind:")
label2.pack()

entry2 = tk.Entry(aken)
entry2.pack()

label3 = tk.Label(aken, text="Kategooria_nimi:")
label3.pack()

entry3 = tk.Entry(aken)
entry3.pack()

label4 = tk.Label(aken, text="Brandi_nimi:")
label4.pack()

entry4 = tk.Entry(aken)
entry4.pack()

btn = tk.Button(aken, text="lisada", command=lambda: Andmed(entry1, entry2, entry3, entry4))
btn.pack()

aken.mainloop()

execute_query(conn, create_brandid_table) 
execute_query(conn, create_kategooriad_table) 
execute_query(conn, create_tooted_table) 
execute_query(conn, insert_brandid) 
execute_query(conn, insert_kategooriad) 
execute_query(conn, insert_tooted)

tooted = execute_read_query(conn, select_tooted)
print("tabel 1:")
for tooted_list in tooted:
    print(tooted_list)

kategooriad = execute_read_query(conn, select_kategooriad)
print("tabel 2:")
for kategooriad_list in kategooriad:
    print(kategooriad_list)

brandid = execute_read_query(conn, select_brandid)
print("tabel 3:")
for brandid_list in brandid:
    print(brandid_list)

insert_tooted = (
    input("toote_nimi:"),
    input("hind:"),
    input("kategooria_id:"),
    input("brandi_id:")
)

insert_kategooriad = (
    input("kategooria_nimi:")
)

insert_brandid = (
    input("brandi_nimi:")
)

tooted_query(conn, insert_tooted)
kategooriad_query(conn, insert_kategooriad)
brandid_query(conn, insert_brandid) 


