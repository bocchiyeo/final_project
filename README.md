# Anime Goods Finder
#### Video Demo: https://www.youtube.com/watch?v=RbqKv1_Uqn4
#### Description:
The rationale behind me choosing this project, is that I usually shop online for anime merchandise, and find that I have to usually search many different sites not only to compare prices, but also to check availability and for items that are in the market. Therefore, I built a website combining searches from the 2 sites that I usually use, AmiAmi and MercariJP. 

For the tech stack, I chose to stick with what CS50 taught for web dev, using HTML, CSS and JS for the frontend, and Quart for the backend.

I wanted to learn to use react for the frontend, but found myself still lacking certain JavaScript or TypeScript fundamentals, deferring my learning to later on in my journey as I plan to take CS50p or CS50w after completing CS50x. For the backend, I decided to use Quart, which is a framework that builds on Flask, implementing async and await functions into the web app. This is particularly useful for search engines as Python can wait for the search to complete before moving on to reading the next line.

The first thing I worked on is with the frontend, using bootstrap classes for the design elements. I had many problems trying to design the website, and used the aid of AI to help me piece together certain design element ideas that I had. I ended up building a pretty generic looking site, with a top bar and cards to represent different items. I also implemented a light and dark mode using JS, to copy how modern sites have those two modes as well. I also implemented a favicon for the website, using a favicon generator and just linking it.

The backend for app.py itself is pretty straightforward, with decorator functions to deal with each site. For the Mercari search, it was pretty easy to implement as I found an API wrapper in Github called Mercapi, with simple functions to call to get the JSON of the items' description by putting the item's name as an argument. However, when it came to AmiAmi, not only did the API require an API key, there was also no reliable Github library that I could import. So I decided to make a webscraper to scrape the item's data when searching and looking at the categories. The details of the scraper can be seen in amiami_scraper.py. I wanted to use BeautifulSoup4 to parse the HTML and put the data into a hashtable(dictionary), but AmiAmi's website requires JS to be enabled to enter the site. Furthermore, running the script returned an error 403, which means forbidden after a quick Google search. It appeared that CloudFlare blocked my request. So I discovered another library called Selenium, which uses chromedriver to automate actions made on the browser. It was pretty hard to implement the scraper as you have to find a class or Xpath that is general for all the loaded items, and also have to piece the algorithm properly to ensure everything on the site is loaded before taking the information from the HTML and storing it in a hashtable(dictionary). I am pretty happy with the results, but one thing that I think can be improved is the runtime as Selenium is pretty slow, especially when waiting for sites to load and scrolling down to load the elements that have lazy loading. I used try and except due to the fact that some items loaded might lack certain elements, in which I have to ignore the errors thrown by Python and continue getting the other elements so that the entire search does not return None.

Asyncio library was used to allow my Selenium functions to run with the app as selenium only uses sync functions.

After implementing the search functions, I went to make 3 categories on the index page. Figures, Plushies and Posters. These are used to look at newly released items so that the user can get a rough idea of what is on the market before using the search function to search through using both search engines. Therefore, I reused the AmiAmi scraper but created a new function to parse the said categories of AmiAmi. To my surprise, AmiAmi did not have a Posters category, so I decided to use the search scraper to search for the word "Poster" and return the products shown on the first 2 pages.

Overall, I am happy with the outcome of my first project, however, improvements like speeding up my AmiAmi searches and also adding more sites to search from can be implemented. (But I am certain that adding too many sites can also cause the search speed to deteriorate exponentially)
