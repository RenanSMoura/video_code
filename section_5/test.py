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
    (3, 'cenoura', 'eee'),
    (4, 'cacau', 'tttt'),
    (5, 'pipoca', 'asdf'),
    (6, 'tati', 'asdf')
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
