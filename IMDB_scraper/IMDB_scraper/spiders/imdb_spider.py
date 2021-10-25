# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    #our scraper!

    # name of our scraper, to be called when we crawl.
    name = 'imdb_spider'
    
    # this is the url of my favorite movie, the Butterfly Effect.
    start_urls = ['https://www.imdb.com/title/tt0289879/']

    # 

    def parse(self,response):
        """
        Starts on the start_urls and navigates to the Cast&Crew page

        Note that the Cast&Crew page has url ending ~ "fullcredits/"
        """

        cast_crew = response.urljoin("fullcredits/")
        yield scrapy.Request(cast_crew, callback = self.parse_full_credits)

    def parse_full_credits(self,response):
        """
        Assume we start on the Cast&Crew page,

        Yield a scrapy.Request for the page of each actor listed on the page.

        Crew members are excluded.
        """

        actors_urls = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        urls = [response.urljoin(a) for a in actors_urls]

        for url in urls:
            yield scrapy.Request(url, callback = self.parse_actor_page)
        
    def parse_actor_page(self,response):
        """
        Assume we start on the page of an actor

        Yield a dictionary in form {"actor" : actor_name,
        "movie_or_TV_name" : movie_or_TV_name}

        This is a dictionary for each of the movies or TV shows
        in which the actor has worked.
        """

        actor_name = response.css("span.itemprop::text")[0].get()

        movies_or_TV_shows_names = [a.css("a::text").get() for a in response.css("div.filmo-row")]

        for item in movies_or_TV_shows_names:
            yield {
                "actor" : actor_name,
                "movie_or_TV_name": item
            }
        
