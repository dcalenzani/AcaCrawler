# AcaCrawler (v.1.3) 

Aca Crawler is an academic crawler for SciELO. Its main focus is to provide the user with a CSV of the articles found for an inserted keyword with their abstract, authors, country, keywords and DOI. But its goal its to become a helper to the initial digging for information found online freely.

<!-- vim-markdown-toc GFM -->

* [Requirements](#requirements)
* [Instructions](#instructions)
* [Log](#log)
        * [V.1.3](#v13)
        * [V.1.2](#v12)
        * [V.1.1](#v11)
        * [V.1.0](#v10)
        * [Backlog (in order of importance)](#backlog-in-order-of-importance)
* [Getting the page structure](#getting-the-page-structure)
* [Further notes for future implementation](#further-notes-for-future-implementation)

<!-- vim-markdown-toc -->

## Requirements
For AcaCrawler to work, you'll need to install python and some dependencies. 
- Python 3.10 (or above)
- PyQt 5 (only if you wish to work on the UI/experimental version)
- BeautifulSoup

We are working on an UI solution that will be distributed online when reaches test level.

## Instructions

For using the program through the CLI, you need to follow the next steps:

1. The cli version will prompt the user for a search term, you can input words and also full phrases. The search term will be used to search in the Scielo database.
2. A prompt with the total amount of pages will be shown, write as input the value for the amount of pages you wish to analyze.
3. Wait while the program is working, it will show the progress of the pages being analyzed.
4. Check the output file, it will be named "[SEARCH TERM].csv" and will be located in the same folder as the program.

## Log
The log contains the information of this version, the previous ones and the planned implementations.

#### V.1.3
- Limiter created
- Functions for counting the total of articles and pages added
- Main program translated all into functions to easen up its integration with UI
- PyQt6 UI functional so more researchers can use the tool (still in test)

#### V.1.2
- Loop for accesing all the articles in all pages of Scielo
- Functions for updating the url dynamic handling of the URL
- Prints for the user the progress of the page handling (at console)
- Variables for pages and approximate (+15) number of articles
- Added DOI and Country tags to the output

#### V.1.1
- Crawler gathers Authors, Title, Abstract and Id from the first page of Scielo
- Crawler changed dictionary and arrays for a dictionary with classes, which are somesort of the same thing actually? But easier to call in a Python environment I guess
- Divided some functions into smaller functions so they could be worked with more flexibility 

#### V.1.0
- Crawler gets the titles and authors information from the first page of scielo

#### Backlog (in order of importance)
- Packaging for alpha version
- XLS format and perhaps just TXT too
- Functions for searching in DOAJ
- Graph creation through matplotlib and networkx libraries
- Functions for searching in Redalyc
- OpenTranslate Abstract translations

## Getting the page structure
For each page we have different HTML structures. In fact, HTML is such a dumpster fire that you can find many libraries that will help you with the random stuff you can find produced by a rage infused coder at 4am.

If you are unfamiliar with HTML I would recommend just using the developer tools and then the tool that says "pick an element" or something along the lines. In Firefox you can use CTRL+SHIFT+C or find the button on the upper left side of the developer tools window.
After doing this you should see the HTML code for the webpage and your cursor acting like a highlighter depending on its position on the site. You can see the HTML code moving, you can right click to copy the inner and outer HTML, I would recommend copying the outer html from the parent `<div>` (usually div) where you wanted contents are contained, always try to find the bigger container (the grand grand grand parent, if you wish). 

Scielo is a more regular webpage, and seems to be statically loaded after gathering the information from the db server. Redalyc on the other side seems to be more dinamically, so it uses only one URL for all the article pages.

## Further notes for future implementation
Please note the current analysis on the Scielo website.
- Scielo uses `<a>` for its next page buttons, while also using "javascript:go_to_page('2')". This can be useful for making the loop for all the pages. But the URL also lets you calculate the length of pages.
- Author are inside a `<div>` called  line authors, inside theres `<a>` with the authors names.
- All the ids inside class="results" have the same lenght, also at the end the define the country (pry=Peru, mex=Mexico, etc), but the ids for class='abstract' have 3 more characters that correspond to the language of the abstract.
- There is an href DOI inside an `<a>` 
