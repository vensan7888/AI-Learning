from .newsPuller import NewsPuller
from common import VectorDataStore

class DynamicKnowledge:
    def __init__(self):
        self.newsPuller = NewsPuller()
        self.vectorData = VectorDataStore()
    
    def retrieve(self, query, k=0):
        news = self.fetchNews(query)
        self.vectorData.add_documents(news)
        answer = self.vectorData.retrieve(query, k)
        return answer
        
    def fetchNews(self, query):
        news = []
        newsApiResults = self.newsPuller.fetchNewsFromNewsApi(query, "latest", "general")
        mediastackApiResults = self.newsPuller.fetchNewsFromMediastack(query, "latest", "general")
        newsDataApiResults = self.newsPuller.fetchNewsFromNewsData(query, "latest", "general")
        news += newsApiResults
        news += mediastackApiResults
        news += newsDataApiResults
        return news
    