import sqlite3

connection = sqlite3.connect("medical.db")

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM reports")

count = cursor.fetchone()[0]

print(f"Total Reports in Database: {count}")

connection.close()