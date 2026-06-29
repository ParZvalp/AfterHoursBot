import sqlite3

conn = sqlite3.connect("afterhours.db")

cursor = conn.execute("PRAGMA table_info(games)")

for column in cursor.fetchall():
    print(column)