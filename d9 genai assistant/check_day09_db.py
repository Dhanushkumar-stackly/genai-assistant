import sqlite3

DB_PATH = "db/day09.sqlite3"

connection = sqlite3.connect(DB_PATH)

cursor = connection.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
)

tables = cursor.fetchall()

print("=" * 60)
print("DAY 09 DATABASE TABLES")
print("=" * 60)

for table in tables:
    print(table[0])

print("=" * 60)

connection.close()