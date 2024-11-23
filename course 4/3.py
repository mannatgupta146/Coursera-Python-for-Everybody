import sqlite3
import requests

# Step 1: Download the mbox.txt file
url = 'https://www.py4e.com/code3/mbox.txt?PHPSESSID=e9606f5c31a20a6e0a78ae79610ebaad'
response = requests.get(url)
file_path = 'mbox.txt'

# Save the file locally
with open(file_path, 'wb') as file:
    file.write(response.content)

# Step 2: Connect to SQLite database
conn = sqlite3.connect('email_counts.sqlite')
cursor = conn.cursor()

# Create the Counts table
cursor.execute('DROP TABLE IF EXISTS Counts;')  # Clear the table if it exists
cursor.execute('CREATE TABLE Counts (org TEXT, count INTEGER);')

# Step 3: Read the mbox file and count emails
with open(file_path, 'r') as file:
    for line in file:
        if line.startswith('From '):
            email = line.split()[1]
            domain = email.split('@')[1]

            cursor.execute('SELECT count FROM Counts WHERE org = ?', (domain,))
            row = cursor.fetchone()
            if row is None:
                cursor.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (domain,))
            else:
                cursor.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (domain,))
                
            if cursor.rowcount % 1000 == 0:
                conn.commit()

# Final commit to save any remaining changes
conn.commit()

# Step 4: Print the results
cursor.execute('SELECT org, count FROM Counts ORDER BY count DESC')
for row in cursor.fetchall():
    print(row)

# Close the connection
conn.close()
