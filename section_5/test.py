import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id int PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

user = (1, 'jose', 'asdf')

insert_query = "INSERT INTO users VALUES(?,?,?)"

cursor.execute(insert_query, user)

users = [
    (2, 'jose', 'asdf'),
    (3, 'jose', 'asdf'),
    (4, 'jose', 'asdf'),
    (5, 'jose', 'asdf'),
    (6, 'jose', 'asdf')
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
