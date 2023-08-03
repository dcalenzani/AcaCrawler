''' The objective of this small script will be to extract the abstracts and data from a first line in Redalyc using only BS4. Selenium could do the trick, but it seems a little bit bloated? It might be because its use case is not scrapping, but web testing. Im sticking with my good soup for now'''

from bs4 import BeautifulSoup # Parsing and handling HTML Tree
from PyQt6.QtGui import QApplication
from PyQt6.QtCore import Qurl
from PyQt6.QtWebEngineWidgets import QWebPage
import ssl # SSL HTTPS Certificates
import csv # CSV handling
import urllib.request, urllib.parse, urllib.error #URL encoding and handling
from urllib.parse import quote
import sys

class Client(QWebPage):
    
    def __init__(self,url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self.on_page_load)
        self.mainFrame().load(Qurl(url))
        self.app.exec_()

    def on_page_load(self):
        self.app.quit()

url =  'https://www.redalyc.org/busquedaArticuloFiltros.oa?q=infraestructura'
client_response = Client(url)
source = client_response.mainFrame().toHtml()

#source = urllib.request.urlopen('https://www.redalyc.org/busquedaArticuloFiltros.oa?q=infraestructura')
soup = BeautifulSoup(source, 'lxml')
js_test = soup.find('p', class_ ='jstest')
print(js_test.text)
