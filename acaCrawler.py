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
def get_soup(url_search):    
    html = urllib.request.urlopen(url_search, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')

    return soup

# Function for updating the base url given some sort of search text and values
def update_url(raw_search,page_number,starting_article):
    parsed_search = urllib.parse.quote(raw_search)
    scielo_base_url = f'https://search.scielo.org/?lang=es&count=15&from={starting_article}&output=site&sort=&format=summary&fb=&page={page_number}&q='
    # redalyc_base_url = 'https://www.redalyc.org/busquedaArticuloFiltros.oa?q=motivaciones'
    url_search = scielo_base_url + parsed_search

    return url_search

def scrape_articles_data(raw_search, limiter, progress_callback): 
    # Process the data and print the progress
    page_number = 1
    starting_article = 1
    articles_per_page = 15
    url_search = update_url(raw_search, page_number, starting_article)
    base_soup = get_soup(url_search)
    while page_number <= limiter:
        # Print progress
        if progress_callback:
            progress_callback(f"Procesando pagina {page_number} de {limiter}: {url_search}")
        # Get all the articles related to the search
        all_articles = get_data(url_search)
        # Update the url
        starting_article = starting_article + articles_per_page
        page_number = page_number + 1
        url_search = update_url(raw_search, page_number, starting_article)

    return all_articles

def get_total_articles(url_search):
    soup = get_soup(url_search).find('strong', id='TotalHits')
    total_articles = soup.get_text().replace(' ', '')
    return total_articles

def get_total_pages(url_search):
    soup = get_soup(url_search).find('input', class_='form-control goto_page')
    # Get the total number of pages (as integer) from our search
    total_pages = int(soup.contents[0].strip().split()[1])

    return total_pages

def get_current_page(url_search):
    soup = get_soup(url_search)
    input_tag = soup.find('input', {'type': 'text', 'name': 'page', 'class': 'form-control goto_page'})

    # Extract the value attribute from the <input> tag
    value = input_tag['value']

    return value

def create_csv(raw_search, all_articles):
    # Define the fieldnames for the .csv (same as classes, might be a more dynamic solution)
    fieldnames = ['Id', 'Title', 'Authors', 'Abstracts', 'DOI', 'Country']

    # Create a .csv files named as the searched text
    with open(f'{raw_search}.csv', 'w', newline='') as file:
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

# The big boy (or girl) - It works by asking for a URL, which can (and will be) the search input we asked for at the beggining
def get_data(url): 
    # Get all the tags that match certain condition of attribute
    def get_tag_and_attr(tag,attr):
        tags = get_soup(url).find_all(tag, class_=attr)      
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

def run_aca_crawler():
    # User search input (parsed)
    def printer_caller(message):
        print(message)

    raw_search = input('Ingrese su busqueda: ')

    # Update the url for the first page
    url_search = update_url(raw_search, 1, 1)

    print(url_search)

    aprox_articles = get_total_articles(url_search)
    total_n_pages = get_total_pages(url_search)
    # Print some information about the findings and ask the number of pages to crawl.
    print('Encontramos un aprox. de : ', aprox_articles, ' articulos')
    print('Estan repartidos entre: ',total_n_pages, ' paginas')

    limiter = int(input('Ingrese el numero de páginas para tabular: '))

    all_articles = scrape_articles_data(raw_search, limiter,printer_caller)

    # Print results
    print('Articulos tabulados: ', len(all_articles))
    
    # CSV function invocation
    create_csv(raw_search, all_articles)
    print("CSV creado de manera exitosa!.")

if __name__ == "__main__":
    # Call the main function with user input
    run_aca_crawler()