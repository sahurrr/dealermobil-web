import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer_name TEXT NOT NULL,
    buyer_phone TEXT NOT NULL,
    car_name TEXT NOT NULL,
    car_year TEXT NOT NULL
)
''')

conn.commit()
conn.close()
print("Tabel 'purchases' berhasil dibuat.")
