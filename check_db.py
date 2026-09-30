import sqlite3

conn = sqlite3.connect("leave.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM leave_requests")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()