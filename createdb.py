import sqlite3

conn = sqlite3.connect("hotel_db.sqlite")
c = conn.cursor()

c.execute("PRAGMA table_info(Type_Chambre)")
for col in c.fetchall():
    print(col)

conn.close()
