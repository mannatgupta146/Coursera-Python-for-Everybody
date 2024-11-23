import urllib.parse
import urllib.request
import json

# Prompt for the location
location = input("Enter location: ")

# Encode the location for the URL
params = {'q': location}
url = 'http://py4e-data.dr-chuck.net/opengeo?' + urllib.parse.urlencode(params)

print(f'Retrieving {url}')

# Retrieve the data from the URL
response = urllib.request.urlopen(url)
data = response.read()

print(f'Retrieved {len(data)} characters')

# Parse the JSON response
info = json.loads(data)

# Print the entire JSON response to debug
print(json.dumps(info, indent=4))

# Access the plus_code from the first feature
if 'features' in info and len(info['features']) > 0:
    plus_code = info['features'][0]['properties']['plus_code']
    print(f'Plus code {plus_code}')
else:
    print("plus_code not found in the response.")
