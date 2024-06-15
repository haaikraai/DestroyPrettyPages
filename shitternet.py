import requests
from bs4 import BeautifulSoup
import pyquery
import attrs
import dataclasses
# import typing
# from abc import *
p = pyquery.pyquery.PyQuery()

def getSoup(url: str) -> BeautifulSoup | None:
    response = requests.get(url)
    if response.status_code != 200:
        print('Error getting url: {url}'.format(url))
        return None
    else:
        soup = BeautifulSoup(response.text)
        return soup


'''
Two main classes:
The first is the base page, the user end product.
It will find all the links, keep the html and pdf the merged results.

The second focuses on a single page.
It will access the url and get rid of all the unneeded, keeping the wanted.
It adds the CSS maybe too?
'''

class GoodbyeSite:
    def __init__(self, main_url):
        self.baseurl = main_url
        self.rules: RuleType = RuleType.getRuleSet(self.baseurl)
        self.soup = getSoup(self.baseurl)
    
    def baseurl(self, url: str):
        self.baseurl = url
        return self.baseurl
        
    @property
    def links(self) -> list:
        section = self.soup.select_one(self.rules.links_selector)
        self.links = section.find_all('a')
        print('getter done for links')
        return self.links




    



# @ABCMeta  
# Convert to dataclass rather
class RuleType:
    def __init__(self):
        self.str_id = ''    # the identifier by string, generally the domain name
        self.title_selector = {'element': 'h1'}        # the css selector to grab the title of the article
        self.content_selector = {'class': 'main'}     # css selector for main text
        self.linksection_selector = {'class': 'nav'}    # css selector for nav links of all articles
        self.link_selector
        self.exclude = 'a'
        
    @classmethod
    def check_duplicates(self, url):
        self.soup = DestroyPrettyPage.getSoup(url)

        print('checking title')
        soup_find = self.soup.find_all(self.title_selector)
        print(soup_find)

        print('checking content')
        soup_find = self.soup.find_all(self.content_selector)
        print(soup_find)

        print('checking links')        
        soup_find = self.soup.find_all(self.linksection_selector)
        print(soup_find)


    

    def getRuleSet(self, url: str):
        # FROM DB
        staticrules = RuleType()
        if "javatpoint.com" in url:
            staticrules.str_id = 'javatpoint.com'
            staticrules.content_selector = {'id': '#city'}
            staticrules.title_selector = {'element':'h1'}
            staticrules.linksection_selector = {'class': '.leftmenu'}
        return staticrules
    



class DestroyPrettyPage:
    def __init__(self, page_url: str, rule_set: RuleType):
        self.pageurl = page_url
        self.rules = RuleType()
        self.soup = getSoup(page_url)
        

    @staticmethod
    def getSoup(url: str) -> BeautifulSoup | None:
        response = requests.get(url)
        if response.status_code != 200:
            print('Error getting url: {url}'.format(url))
            return None
        else:
            soup = BeautifulSoup(response.text)
            return soup    


def get_test_urls(cls):
    urls = []
    with open('testurls.txt', 'r') as f:
        print(f.readline())
        urls = f.readlines()
    return urls

urls = get_test_urls()

print('trying this site: {}'.format(urls[4]))
site = GoodbyeSite(urls[4])

if __name__=="__main__":
    url0 = 'https://www.gumtree.co.za/'
    url1 = 'https://www.javatpoint.com/android-tutorial'
    site = GoodbyeSite(urls[0])

clean = DestroyPrettyPage(url1, RuleType.getRuleSet(url1))
all = clean.soup.find_all(True)
# for i,a in enumerate(all):
#     print(i, '-', a)

d = clean.strip_makeup(clean.soup)