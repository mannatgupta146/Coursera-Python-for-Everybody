import urllib.request, urllib.parse, urllib.error
import sqlite3
import json
import ssl

# API endpoint
serviceurl = 'https://py4e-data.dr-chuck.net/opengeo?'

# Connect to SQLite database
conn = sqlite3.connect('opengeo.sqlite')
cur = conn.cursor()

# Create table if it doesn't exist
cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Open the file with location data
fh = open("where.data")
count = 0
nofound = 0

# Process only the first 10 locations
for line in fh:
    if count >= 10:
        print('Retrieved 10 locations, stopping.')
        break

    address = line.strip()
    print('')

    # Check if the location is already in the database
    cur.execute("SELECT geodata FROM Locations WHERE address= ?",
                (memoryview(address.encode()), ))

    try:
        data = cur.fetchone()[0]
        print("Found in database", address)
        continue
    except:
        pass

    # Build the URL with the address as a parameter
    parms = dict()
    parms['q'] = address
    url = serviceurl + urllib.parse.urlencode(parms)

    # Retrieve the data from the API
    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')

    count += 1

    try:
        js = json.loads(data)
    except:
        print('Failed to parse JSON')
        continue

    if not js or 'features' not in js or len(js['features']) == 0:
        print('==== Object not found ====')
        nofound += 1
        continue

    # Insert the retrieved data into the database
    cur.execute('''INSERT INTO Locations (address, geodata)
                   VALUES ( ?, ? )''',
                (memoryview(address.encode()), memoryview(data.encode())))

    conn.commit()

# Summary
if nofound > 0:
    print('Number of locations not found:', nofound)

print("Run geodump.py to read the data from the database.")