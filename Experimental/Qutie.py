from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import QtWidgets, uic
import sys
# Libraries for the implementation
from bs4 import BeautifulSoup # Parsing and handling HTML Tree
import ssl # SSL HTTPS Certificates
import csv # CSV handling
import urllib.request, urllib.parse, urllib.error #URL encoding and handling
from urllib.parse import quote
from GraphiCrawl import Ui_Form

# Ignore SSL errors (Scielo and Redalyc are trustable, I guess, but be careful as server impersonation might be possible (even thought unlikely)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Scielo URL navigational variables
articles_per_page = 15
starting_article = 1
page_number = 1

# Classes and variables
articles = {} # Dictionary for placing Article objects
class Article: # Class for placing Article attributes

    def __init__(self):
        self.doi = None
        self.country = None
        self.title = None
        self.authors = []
        self.abstracts = []

class MainWindow(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

# Functions
# Make the soup - Handle the web page
def soup(url):    
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

# Function for updating the base url given some sort of search text and values
def update_url(search_text,page_number,starting_article):
    
    scielo_base_url = f'https://search.scielo.org/?lang=es&count=15&from={starting_article}&output=site&sort=&format=summary&fb=&page={page_number}&q='
    # redalyc_base_url = 'https://www.redalyc.org/busquedaArticuloFiltros.oa?q=motivaciones'
    scielo_search = scielo_base_url + search_text

    return scielo_search

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
            articles[div_id].country = div_id[-3:]
        match attr:
            case 'title':
                articles[div_id].title = name
            case 'author':
                articles[div_id].authors.append(name)
            case 'abstract':
                articles[div_id].abstracts.append(name)
            case 'DOIResults':
                articles[div_id].doi = name
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

    for tag in get_tag_and_attr('span', 'DOIResults'):
        get_parent_id(tag)
        class_filler(tag, 'DOIResults')
    
    return articles

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()