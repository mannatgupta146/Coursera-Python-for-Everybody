import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('rosterdb.sqlite')
cursor = conn.cursor()

# First query
cursor.execute('''
    SELECT User.name,Course.title, Member.role FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY User.name DESC, Course.title DESC, Member.role DESC LIMIT 2;
''')

first_query_results = cursor.fetchall()
for row in first_query_results:
    print('|'.join(map(str, row)))

# Second query
cursor.execute('''
    SELECT 'XYZZY' || hex(User.name || Course.title || Member.role ) AS X FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X LIMIT 1;
''')

second_query_result = cursor.fetchone()
print(second_query_result[0])

# Close the connection
conn.close()
