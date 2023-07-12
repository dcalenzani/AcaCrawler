# AcaCrawler (v.1.1) 
Aca Crawler is the academic crawler for SciELO and REDALYC. Its main focus is to provide the user with a CSV of the articles found for an inserted keyword with their abstract, authors, country, keywords and DOI. But its goal its to become a helper to the initial digging for information found online freely. I always have random themes of research in my mind which I would like to quickly grasp to see if they capture my attention, so this intends to be a tool to this purpose too.

The code is extensively commented, as I currently still feel jupiter notebooks are sluggish unless you are giving a report of some sort. 

## Log
The log contains the information of this version, the previous ones and the planned implementations.

#### V.1.1
- Crawler gathers Authors, Title, Abstract and Id from the first page of Scielo
- Crawler changed dictionary and arrays for a dictionary with classes, which are somesort of the same thing actually? But easier to call in a Python environment I guess
- Divided some functions into smaller functions so they could be worked with more flexibility 

#### Planned implementations (in order of importance)
- Return to the user the number of pages and approximate number of articles
- Loop for accesing the articles in the other pages of the search
- Graph creation through matplotlib and networkx libraries
- Functions for searching in Redalyc
- Return to the user the progress with the CSV

## Getting the page structure
For each page we have different HTML structures. In fact, HTML is such a dumpster fire that you can find many libraries that will help you with the random stuff you can find produced by a rage infused coder at 4am.

If you are unfamiliar with HTML I would recommend just using the developer tools and then the tool that says "pick an element" or something along the lines. In Firefox you can use CTRL+SHIFT+C or find the button on the upper left side of the developer tools window.
After doing this you should see the HTML code for the webpage and your cursor acting like a highlighter depending on its position on the site. You can see the HTML code moving, you can right click to copy the inner and outer HTML, I would recommend copying the outer html from the parent `<div>` (usually div) where you wanted contents are contained, always try to find the bigger container (the grand grand grand parent, if you wish). 

### Further notes for future implementation
Please note the current analysis on the Scielo website.
- Scielo uses `<a>` for its next page buttons, while also using "javascript:go_to_page('2')". This can be useful for making the loop for all the pages. But the URL also lets you calculate the length of pages.
- Author are inside a `<div>` called  line authors, inside theres `<a>` with the authors names.
- All the ids inside class="results" have the same lenght, also at the end the define the country (pry=Peru, mex=Mexico, etc), but the ids for class='abstract' have 3 more characters that correspond to the language of the abstract.
- There is an href DOI inside an `<a>` 