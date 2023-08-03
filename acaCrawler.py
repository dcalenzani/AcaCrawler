''' AcaCrawler V.1.1
Academic Crawler for Scielo and Redalyc. Both digital libraries focus on distributing online open access journal, playing one of the most important roles in promoting open access to scientific research, facilitating access to many researchers of the region

Aca Crawler allows the user to automate its research by transforming first search URL into a CSV table with the most relevant data from each article (Authors, DOI (if found), Country, Title, Abstract)

I feel that Jupiter Notebooks are a little bit clunky, so let me know if any of the comments are difficult to understand or maybe more should be added.

The organization of the code goes like this:
1 - Libraries
2 - Boilerplate and variables
3 - Scraping functions
4 - Scraping process
5 - CSV appending
''' 

# Libraries for the implementation
from bs4 import BeautifulSoup # Parsing and handling HTML Tree
import ssl # SSL HTTPS Certificates
import csv # CSV handling
import urllib.request, urllib.parse, urllib.error #URL encoding and handling
from urllib.parse import quote

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

class Article:

    def __init__(self):
        self.doi = None
        self.country = None
        self.title = None
        self.authors = []
        self.abstracts = []

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

def update_loop():
    # Process the data and print the progress
    global page_number, starting_article

    while page_number <= limiter:
        # Print progress
        print(f"Procesando pagina {page_number} de {total_n_pages}: {base_url}")
        # Get all the articles related to the search
        all_articles = get_data(base_url)
        # Update the url
        starting_article = starting_article + articles_per_page
        page_number = page_number+1
        base_url = update_url(search_text, page_number, starting_article)

    return all_articles

def create_csv(search_text, all_articles):
    # Define the fieldnames for the .csv (same as classes, might be a more dynamic solution)
    fieldnames = ['Id', 'Title', 'Authors', 'Abstracts', 'DOI', 'Country']

    # Create a .csv files named as the searched text
    with open(f'{search_text}.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for article_id, article in all_articles.items():
            row = {
                    'Id' : article_id,
                    'Title': article.title,
                    'Authors':', '.join(article.authors),
                    'Abstracts': ', '.join(article.abstracts),
                    'DOI' : article.doi,
                    'Country': article.country
                }
            writer.writerow(row)

def run_aca_crawler(search_text, limiter):
    # Hook the global variables (Python specific)
    global articles_per_page, starting_article, page_number

    # Update the url for the first page
    base_url = update_url(search_text, page_number, starting_article)

    # Search for the tag that contains the text with the total of pages
    input_tag = soup(base_url).find('input', class_='form-control goto_page')

    # Get the total number of pages (as integer) from our search
    total_n_pages = int(input_tag.contents[0].strip().split()[1])

    # Aproximate the number of articles (to lowest)
    aprox_articles = articles_per_page*total_n_pages

    # Print some information about the findings and ask the number of pages to crawl.
    print('Encontramos un aprox. de : ', aprox_articles, ' articulos')
    print('Estan repartidos entre: ',total_n_pages, ' paginas')

    all_articles = get_data(base_url)
    
    # Print results
    total_articles = len(all_articles)
    print('Articulos tabulados: ', len(all_articles))
    articles_processed = 0

    # CSV function invocation
    create_csv(search_text, all_articles)
    print("CSV creado de manera exitosa!.")

if __name__ == "__main__":
    # User search input (parsed)
    search_text = urllib.parse.quote(input('Ingrese su busqueda: '))

    # Update the url for the first page
    base_url = update_url(search_text, page_number, starting_article)

    # Search for the tag that contains the text with the total of pages
    input_tag = soup(base_url).find('input', class_='form-control goto_page')

    # Get the total number of pages (as integer) from our search
    total_n_pages = int(input_tag.contents[0].strip().split()[1])

    # Aproximate the number of articles (to lowest)
    aprox_articles = articles_per_page*total_n_pages

    # Print some information about the findings and ask the number of pages to crawl.
    print('Encontramos un aprox. de : ', aprox_articles, ' articulos')
    print('Estan repartidos entre: ',total_n_pages, ' paginas')
    limiter = int(input('Ingrese el numero de páginas para tabular: '))

    # Call the main function with user input
    run_aca_crawler(search_text, limiter)

'''
'''