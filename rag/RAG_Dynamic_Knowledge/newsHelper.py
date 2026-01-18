import re
import ast
import json
from enum import Enum

class NewsProvider(Enum):
    NewsApi = 1
    Mediastack = 2
    NewsData = 3
    
    def titleKey(self) -> str:
        match self:
            case NewsProvider.NewsApi | NewsProvider.Mediastack | NewsProvider.NewsData:
                return "title"
            
    def descriptionKey(self) -> str:
        match self:
            case NewsProvider.NewsApi | NewsProvider.Mediastack | NewsProvider.NewsData:
                return "description"
    
    def sourceKey(self) -> str:
        match self:
            case NewsProvider.NewsApi:
                return "source.name"
            case NewsProvider.Mediastack:
                return "source"
            case NewsProvider.NewsData:
                return "source_name"
    
    def urlKey(self) -> str:
        match self:
            case NewsProvider.NewsApi | NewsProvider.Mediastack:
                return "url"
            case NewsProvider.NewsData:
                return "source_url"
    
    def publishedKey(self) -> str:
        match self:
            case NewsProvider.NewsApi:
                return "publishedAt"
            case NewsProvider.Mediastack:
                return "published_at"
            case NewsProvider.NewsData:
                return "pubDate"

class News:
    def __init__(self, data, provider: NewsProvider):
        self.title = self.get_by_keypath(data, provider.titleKey())
        self.description = self.get_by_keypath(data, provider.descriptionKey())
        self.source = self.get_by_keypath(data, provider.sourceKey())
        self.url = self.get_by_keypath(data, provider.urlKey())
        self.publishDate = self.get_by_keypath(data, provider.publishedKey())
    
    def get_by_keypath(self, data, keypath):
        if "." in keypath:
            keys = keypath.split(".") # check if it has "."
            for key in keys:
                data = data[key]
            return data
        else:
            return data[keypath]