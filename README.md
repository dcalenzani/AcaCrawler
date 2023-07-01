# AcaCrawler (v.1) 

Aca Crawler is the academic crawler for SciELO and REDALYC. Its main focus is to provide the user with a CSV of the articles found for an inserted keyword with their abstract, authors, country, keywords and DOI. 

The code is extensively commented, as I currently still hate jupiter notebooks and don't think of them as actually useful unless you are teaching something of some sort. 

Is every text a piece of learning? Thats more of a onthological question, me thinks.

## Graph creation

When the first part of Aca Crawler (csv creation) is done we can do a small graph that links keywords and countries.

## Page Structure

For each page we have different structures for their HTML <tags>. If you are unfamiliar with HTML I would recommend just using the developer tools and then the tool that says "pick an element" or something along the lines. In Firefox you can use CTRL+SHIFT+C. 

After doing this you should see the HTML code for the webpage and your cursor acting like a highlighter depending on its position on the site. Select your desired object for analysis an copy its tag. 

### Examples provided

For example, the webpage Scielo uses a <strong>, but this is contained inside and <a> tag, so you could use any of them for their links to the articles pages. As <a> is more usual insider the webpage my solution searches first for the unique strong tag and then compares it with the <a> tag title

I checked the following [search](https://search.scielo.org/?lang=en&count=15&from=0&output=site&sort=&format=summary&fb=&page=1&q=suicidio) that you can use as an example.

When going inside an [article page](https://www.scielo.br/j/rlae/a/bJjynbR36qqNrskkRhF9k7k/?lang=es) and using CTRL+SHIFT+C again we'll see things get a little complicated, as the Abstract is just a <div> before a <dif> with an article tag and the authors of the article are hidden within a modal that uses the <div> tag again, with a class='modal-body' that containg a <div class='tutors'> which contains the data we require.

https://www.redalyc.org/busquedaArticuloFiltros.oa?q=suicidio

https://www.redalyc.org/articulo.oa?id=203122516002