import re

# Prompt the user to enter the filename
name = input("Enter file:")

# Use 'test.txt' as the default file if no name is provided
if len(name) < 1:
    name = "text.txt"  # Make sure to use your actual data file

# Open the file
fh = open(name)

# Initialize an empty list to store numbers
newlist = []

# Iterate through each line in the file
for line in fh:
    # Find all numbers in the line using regular expressions
    numbers = re.findall('[0-9]+', line)
    # Convert each found number to an integer and add to the list
    for number in numbers:
        newlist.append(int(number))

# Compute and print the sum of all numbers
print(sum(newlist))
