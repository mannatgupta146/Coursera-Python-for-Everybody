import sqlite3

# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create the Ages table
cursor.execute('''
CREATE TABLE Ages (
    name VARCHAR(128),
    age INTEGER
)
''')

# Insert data into the Ages table
data = [
    ('Nevaeh', 17),
    ('Tiana', 20),
    ('Iagan', 20),
    ('Elyce', 17),
    ('Mack', 19),
    ('Calah', 23)
]
cursor.executemany('INSERT INTO Ages (name, age) VALUES (?, ?)', data)

# Query to retrieve the hexadecimal representation
cursor.execute('''
SELECT hex(name || age) AS X 
FROM Ages 
ORDER BY X
''')

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row[0])

# Close the connection
conn.close()
