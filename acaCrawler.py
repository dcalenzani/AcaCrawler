# OK so this is going to be an academic crawler, but for fun I'm starting with a dnd page that I know won't have that many constraints as other APIs

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import csv

# Crawler

slate = list()
url = input('Enter the url:\n')

# 1st and always, you've gotta ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Handle the web page
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

# Search the <strong> tags
tags = soup.find_all('strong')

def has_class_title(tag):
    return tag.has_attr('title')

# Retrieve all of the <strong> tags
for tag in tags:
    # Look at the contents of a tag
    contents = tag.contents
    if contents:
        # Print the contents
        print('Contents:', contents[0])
        # Append in the slate
        slate.append(contents[0])

print(slate)

with open('tabulate.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows([[item] for item in slate])