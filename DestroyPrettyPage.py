import requests
from bs4 import BeautifulSoup, Tag
import urllib.parse
from typing import Optional, NamedTuple
import lxml




class RuleType(NamedTuple):
    """
    Represents a rule for extracting content from a specific website.

    Attributes:
        str_id (str): The identifier for the website. This is usually just the hostname.
        content_section (str): The CSS selector for the main content section.
        split_content (bool): Indicates whether the article should be split into a title and content. If true, they are concatenated into the content. If false, the content is taken directly with one `select_one` call from the content_section.
        title_selector (str | None): The CSS selector for the title element (if split_content is True).
        article_selector (str): The CSS selector for the article element.
        links_section (str): The CSS selector for the section containing links.
        links_selector (str): The CSS selector for the links within the links_section.
    """

    str_id: str
    content_section: str
    split_content: bool
    title_selector: str | None
    article_selector: str
    links_section: str
    links_selector: str

    @classmethod
    def getRuleSet(cls, url):
        """
        Returns a RuleType object based on the given URL.
        This function currently works for the following websites:
        - www.javatpoint.com

        It uses archaic if-elif-else statements to determine the rules based on the hostname.
        SQLite will be used in the future to store and retrieve rules for different websites.

        Args:
            url (str): The URL of the website.

        Returns:
            RuleType: The RuleType object representing the rules for the website.
        """
        host = urllib.parse.urlparse(url).netloc
        print('host is:' + host)
        
        if "javatpoint.com" in host:
            cls.str_id = host
            cls.content_section = '#city'
            cls.article_selector = '.onlycontentinner'
            cls.split_content = False
            cls.title_selector = 'h1'
            cls.links_section = '#menu'
            cls.links_selector = 'a'
        elif "course.fast.ai" in host:
            cls.str_id = host
            cls.content_section = 'main'
            cls.article_selector = '.content'
            cls.split_content = False
            cls.title_selector = 'h1'
            cls.links_section = 'nav'
            cls.links_selector = 'div.side-bar-item-container a'
        elif "test.html" in host:
            cls.str_id = 'dev_test'
            cls.content_section = '#templatecontainer'
            cls.article_selector = '#flighttemplate'
            cls.split_content = True
            cls.title_selector = 'h1'
            cls.links_section = '#fltemplate'
            cls.links_selector = 'a'
        else:
            print(f'No rules for {host}. Using default rules.')
            cls.str_id = host
            cls.content_section = 'body'
            cls.article_selector = 'body'
            cls.split_content = False
            cls.title_selector = None
            cls.links_section = 'body'
            cls.links_selector = 'a'
        return cls



class DestroyPrettyPage:
    """
    A class parsing a site subdomain to extract the text value from it eliminating paging, headers, toolbars, footers, etc.
    Own simple CSS is applied afterwards.
    
    Args:
        base_url (str): The base URL of the website to destroy.
    
    Attributes:
        baseurl (str): The base URL of the website.
        rules (RuleType): The rules for destroying the website.
        soup (BeautifulSoup): The BeautifulSoup object representing the website's HTML.
        title (str): The title of the website.
        article (str): The article content of the website.
        content (str):* The calculated content of the website.
        pagelinks (list[str]): The links found on the website.
    """
    
    def __init__(self, base_url: str):
        if not base_url.startswith('http'):
            print('Invalid URL. Initiating development mode.')
            self._dev_init()
        else:
            self.baseurl = base_url

            self.rules: RuleType = RuleType.getRuleSet(self.baseurl)
            self.soup: BeautifulSoup = self.getSoup(self.baseurl)
            # self.getContent()
            # parsed values
        self._title = ''
        self._article = ''
        self.html = self.soup.prettify()
        self.content = self.soup.new_tag('div', attrs={'class': "parsed",
                                                       "id": 'parsed_content'})
        # Calculated values:
        self.parsed = False
        try:
            self.pagelinks = self.getLinks()
            for link in self.pagelinks:
                self.content = self.getContent(self.html)
                self.parsed = True
        except Exception as e:
            print('Error parsing the website')
            print(f'URL: {self.baseurl}. Error: {e}')
            
    def _dev_init(self):
        """
        Initialize the class for development purposes.
        Uses test.html file for the html
        """
        self.baseurl: str = 'file://test.html'
        self.rules: RuleType = RuleType.getRuleSet(self.baseurl)


        with open('test.html', 'rt') as fh:
            self.soup: BeautifulSoup = BeautifulSoup(fh, 'html.parser')


    @property
    def nr_of_pages(self):
        return len(self.pagelinks)

    def getLinks(self) -> list[str]:
        """
        Get the links from the website.
        
        Returns:
            list[str]: A list of urls found on the website.
        """
        hrefs = []
        links_area = self.soup.select_one(self.rules.links_section)
        links = links_area.select(self.rules.links_selector)
        # print(links_area)
        print('**********\n\n\n\n\n\n')
        for i, link in enumerate(links):
            link_url = self.baseurl + '/' + link['href']
            printout = f"{i}) {link.text}\t-\t{link['href']}"
            print(printout)
            hrefs.append(link_url)
        self.links = links
        return links
    
    def getContent(self, pageTag: Tag):
        """
        Retrieves the content of the web page.

        Returns:
            str: The prettified content of the web page.
        """
        # TODO: Be open for the possibility of multiple content sections, e.g. for different pages. Receive the content section as an soup-type, not an html.
        print('getting content')
        self.content = self.soup.new_tag('div', id='parsed_content')
    
        content_area = self.soup.select_one(self.rules.content_section)
        if self.rules.split_content:
            # self.soup.
            self._title = self.soup.select_one(self.rules.title_selector)
            self._article = self.soup.select_one(self.rules.article_selector)
            print('here')
            # self._title.append(self._article)
            self.content.extend([self._title, self._article])
            # self.content = self._title
            print(self.content)
        else:
            self.content.extend(content_area.select_one(self.rules.article_selector))
        # 
        
        print('got the content')
        print('content: ', self.content)

        # wrap the content in a div
        # print('wrapping content')
        # self.content.wrap(self.content)
        print('content wrapped: ', self.content)
        
        return self.content
    
    def strip_tags(self, htmlTag: Tag) -> str:
        """
        Strips the HTML tags from the given HTML string.
        
        Args:
            html (Tag): The HTML string to strip.
        
        Returns:
            str: The stripped HTML string.
        """
        stripped = htmlTag
        for tag in stripped.find_all(True):
            tag.attrs.clear()
        return stripped.prettify()

    @staticmethod
    def getSoup(url: str) -> BeautifulSoup | None:
        """
        Get the BeautifulSoup object representing the website's HTML.
        
        Args:
            url (str): The URL of the website.
        
        Returns:
            BeautifulSoup | None: The BeautifulSoup object if successful, None otherwise.
        """
        response = requests.get(url)
        soup = None

        try:
            if response.status_code != 200:
                print('Error getting url: {url}'.format(url))
                soup = None
            else:
                soup = BeautifulSoup(response.text, 'lxml')
        except Exception as e:
            print(f'Error getting url: {url} - {e}')
            soup = None
        finally:
            return soup





if __name__ == 'main':
    print('name is main indeed')


print('Not supposed to do this:')
dps = DestroyPrettyPage('dev_test')

