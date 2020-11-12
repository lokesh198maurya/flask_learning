import sqlite3

conection = sqlite3.connect('data.db')

cursor = conection.cursor()

create_table = "CREATE TABLE users ('id' int, 'username' text, 'password' text)"
cursor.execute(create_table)

users = [(1, 'Loki', 'asd520'), (2, 'Lokesh', 'asd420'), (3, 'test', 'asd320')]

insert_query = 'INSERT INTO users VALUES(?, ?, ?)'
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

conection.commit()

conection.close()