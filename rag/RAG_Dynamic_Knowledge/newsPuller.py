import requests
from urllib.parse import quote
from .newsHelper import News
from .newsHelper import NewsProvider

class NewsPuller:
    
    def processResponse(self, response):
        try:
            data = response.json()
        except ValueError:
            # Not a JSON response
            print("Response is not JSON")
            data = []
        return data
    
    # Function to fetch news context
    def fetchNewsFromNewsApi(self, query, keyword, category):
        API_KEY = ""
        print(f"******* Agent has arrived newsApi to fetch News from API query: {query} ********")
        url = "https://newsapi.org/v2/everything"
        escapedQuery = quote(query)
        params = {
            "q": escapedQuery,
            "language": "en",
            "pageSize": 30,   # get top 10 articles
            "sortBy": "relevancy",
            "apiKey": API_KEY
        }
        print("***** Hitting newsApi API ******\n")
        data = self.executeApiRequest(url, params)

        if data.get("status") != "ok":
            return []

        articles = data["articles"]
        print(f"Received News Data {len(articles)}::\n{articles}\n")
        docs = self.formattedArticles(articles, NewsProvider.NewsApi)
        return docs

    def fetchNewsFromMediastack(self, query, keyword, category):
        API_KEY = ""
        print(f"******* Agent has arrived mediastack to fetch News from API query: {query} ********")
        url = "https://api.mediastack.com/v1/news"
        keywords = keyword.replace(" ", ",")
        escapedQuery = quote(query)
        params = {
            "search": query,
            "limit": 100,
            "keywords": keywords,
            "languages": "en",
            "offset": 0,   # get top 10 articles
            "sort": "published_asc",#"popularity",
            "categories": category,
            #"countries": "",
            #"sources": "",
            "access_key": API_KEY
        }
        print("***** Hitting mediastack API ******\n")
        data = self.executeApiRequest(url, params)
        
        if not data["data"]:
            return []

        articles = data["data"]
        print(f"Received News Data {len(articles)}::\n{articles}\n")
        docs = self.formattedArticles(articles, NewsProvider.Mediastack)
        return docs

    def fetchNewsFromNewsData(self, query, keyword, category):
        API_KEY = ""
        print(f"******* Agent has arrived newsData to fetch News from API query: {query} ********")
        url = "https://newsdata.io/api/1/latest"
        escapedQuery = quote(query)
        
        params = {
            "q": keyword,
            "language": "en",
            #"from_date": "2025-09-24",#"popularity",
            #"to_date": "2025-09-24",
            #"country": "",
            "category": category,
            "apikey": API_KEY
        }
        if category == "general":
            del params["category"]

        print("***** Hitting NewsData API ******\n")
        data = self.executeApiRequest(url, params)

        if data["status"] != "success":
            return []

        articles = data["results"]
        print(f"Received News Data {len(articles)}::\n{articles}\n")
        docs = self.formattedArticles(articles, NewsProvider.NewsData)
        return docs

    def executeApiRequest(self, url, params):
        response = requests.get(url, params=params)
        print(f"***** Response Received {response.url} ******\n")
        data = self.processResponse(response=response)
        print(f"API Raw Response:: {response} \n {data}")
        return data
    
    def formattedArticles(self, articles, newProvider):
        docs = []
        for article in articles:
            news = News(article, newProvider)
            content = f"#{news.title} ({news.publishDate}) - {news.description} - ({news.url}),"
            docs.append(content)
        return docs