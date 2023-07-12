''' AcaCrawler V.1.1
Academic Crawler for Scielo and Redalyc. Both digital libraries focus on distributing online open access journal, playing one of the most important roles in promoting open access to scientific research, facilitating access to many researchers of the region
.
Aca Crawler allows the user to automate its research by transforming first search URL into a CSV table with all the results and presenting it into a relational network.

As of now, AcaCrawler only outputs in the CSV the data from the first webpage. But further updates will include all searches.
''' 
# Libraries for the implementation
from bs4 import BeautifulSoup # Parsing and handling HTML Tree
import ssl # SSL HTTPS Certificates
import csv # CSV handling
import urllib.request, urllib.parse, urllib.error #URL encoding and handling
from urllib.parse import quote

# User search input
search_text = input('Ingrese su busqueda: ')
parsed_search = urllib.parse.quote(search_text) # Encode the search string() into url format

# Base urls - The search urls stripped of the search query (right now only Scielo is supported)
scielo_base_url = 'https://search.scielo.org/?lang=es&count=15&from=0&output=site&sort=&format=summary&fb=&page=1&q='

# Ignore SSL errors (Scielo and Redalyc are trustable, I guess, but be careful as server impersonation might be possible even tough unlikely)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Classes and variables
articles = {} # Dictionary for placing Article objects

class Article:
    def __init__(self):
        self.title = None
        self.authors = []
        self.abstracts = []

# Functions

# Make the soup - Handle the web page
def soup(url):    
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

# The big boy (or girl) - It works by asking for a URL, which can (and will be) the search input we asked for at the beggining
def get_data(url):
    
    # Get all the tags that match certain condition of attribute
    def get_tag_and_attr(tag,attr):
        tags = soup(url).find_all(tag, class_=attr)      
        return tags
    
    # Get the "parent id". In Scielo, all articles tags are contained inside a <div> with a key id.
    def get_parent_id(tag):
        div_id = tag.find_parent('div', {'id': True})['id']
        return div_id
    
    # Initiate the Article() with the name of the ID and fill it with the requested information
    def class_filler(tag, attr):
        div_id = get_parent_id(tag) # Get the parent id
        name = tag.text.strip() # Get the tag text (the contents)

        # Check if our Article already exists. If it doesn't we create it, if it does then we append the classes to the corresponding attribute.
        if div_id not in articles:
            articles[div_id] = Article()
        match attr:
            case 'title':
                articles[div_id].title = name
            case 'author':
                articles[div_id].authors.append(name)
            case 'abstract':
                articles[div_id].abstracts.append(name)
        return

    # Get the data for each attribute (is there a less repetitive way of doing this?)
    for tag in get_tag_and_attr('a', 'author'):
        get_parent_id(tag)
        class_filler(tag, 'author')

    for tag in get_tag_and_attr('strong', 'title'):
        get_parent_id(tag)
        class_filler(tag, 'title')

    for tag in get_tag_and_attr('div', 'abstract'):
        get_parent_id(tag)
        class_filler(tag, 'abstract')
    
    return articles

# Mix the search with the base url
scielo_search = scielo_base_url+parsed_search

# Get all the articles related to the search
all_articles = get_data(scielo_search)

# Define the fieldnames for the .csv
fieldnames = ['Id', 'Title', 'Authors', 'Abstracts']

# Create a .csv files named as the searched text
with open(f'{search_text}.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for article_id, article in all_articles.items():
        row = {
                'Id' : article_id,
                'Title': article.title,
                'Authors':', '.join(article.authors),
                'Abstracts': ', '.join(article.abstracts)
            }
        writer.writerow(row)
    print("CSV file created successfully.")

'''
'''