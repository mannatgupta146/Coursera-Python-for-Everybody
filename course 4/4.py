import csv
import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('music.sqlite')  # Updated file name to .sqlite
cur = conn.cursor()

# Create tables
cur.execute('''
CREATE TABLE IF NOT EXISTS Artist (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Genre (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Album (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    title TEXT UNIQUE
)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Track (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id INTEGER,
    genre_id INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
)''')

# Define the column names manually
column_names = ['Name', 'Artist', 'Album', 'Length', 'Rating', 'Count', 'Genre']

# Read CSV file and insert data into tables
with open('tracks.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    
    # Skip the first row if it's empty (if your CSV doesn't have headers)
    next(reader)  # Use this line if there's a header; otherwise, comment it out
    
    for row in reader:
        # Use a dictionary to match column names with row values
        row_dict = {name: value for name, value in zip(column_names, row)}
        
        # Insert Artist
        cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)', (row_dict['Artist'],))
        cur.execute('SELECT id FROM Artist WHERE name = ?', (row_dict['Artist'],))
        artist_id = cur.fetchone()[0]

        # Insert Genre
        cur.execute('INSERT OR IGNORE INTO Genre (name) VALUES (?)', (row_dict['Genre'],))
        cur.execute('SELECT id FROM Genre WHERE name = ?', (row_dict['Genre'],))
        genre_id = cur.fetchone()[0]

        # Insert Album
        cur.execute('INSERT OR IGNORE INTO Album (artist_id, title) VALUES (?, ?)', (artist_id, row_dict['Album']))
        cur.execute('SELECT id FROM Album WHERE title = ?', (row_dict['Album'],))
        album_id = cur.fetchone()[0]

        # Insert Track
        cur.execute('''INSERT OR IGNORE INTO Track (title, album_id, genre_id, len, rating, count)
                       VALUES (?, ?, ?, ?, ?, ?)''',
                   (row_dict['Name'], album_id, genre_id, row_dict['Length'], row_dict['Rating'], row_dict['Count']))

# Commit changes and close the database connection
conn.commit()

# Run a query to check the inserted data
cur.execute('''
SELECT Track.title, Artist.name, Album.title, Genre.name 
FROM Track 
JOIN Genre ON Track.genre_id = Genre.id 
JOIN Album ON Track.album_id = Album.id 
JOIN Artist ON Album.artist_id = Artist.id
ORDER BY Artist.name LIMIT 3
''')

# Print the results of the query
print("Track\tArtist\tAlbum\tGenre")
for row in cur.fetchall():
    print("\t".join(map(str, row)))

# Close the connection
conn.close()
