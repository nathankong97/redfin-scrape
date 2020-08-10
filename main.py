import requests
import lxml.html
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random

class Proxy:
    def __init__(self):
        self.test_url = "https://www.google.com"
        self.ua = UserAgent(verify_ssl=False, use_cache_server=False)
        self.ip_proxies = []

        self.get_ip_proxies()

    def get_ip_proxies(self):
        url = 'http://www.nimadaili.com/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'}
        req = requests.get(url, headers=headers).content.decode()
        req_1 = lxml.html.fromstring(req)
        Ip = req_1.xpath('//tbody[@style="background: #fff;"]/tr/td/text()')
        self.ip_proxies = [elem for elem in Ip if ":" in elem and "." in elem]

    def check_if_ip_valid(self):
        for ip in self.ip_proxies:
            http = "http:\\\{}".format(ip)
            https = "https:\\\{}".format(ip)
            proxy = {'proxy': http}
            try:
                headers = {'User-Agent': self.ua.random}
                s = requests.get(self.test_url, proxies=proxy, headers = headers)
                tree = lxml.html.fromstring(s.content).findtext('.//title')
                print(http, s.status_code, tree)
            except:
                proxy = {'proxy': https}
                headers = {'User-Agent': self.ua.random}
                s = requests.get(self.test_url, proxies=proxy, headers=headers)
                tree = lxml.html.fromstring(s.content).findtext('.//title')
                print(http, s.status_code, tree)

class Redfin:
    def __init__(self, zip_code = "", proxy = None):
        self.proxy = proxy
        self.url = "https://www.redfin.com/zipcode/" + zip_code
        self.zip_code = zip_code
        self.ua = UserAgent(verify_ssl=False, use_cache_server=False)
        self.pages = 1
        self.property_urls = []

        self.get_pages(self.url)
        for page in range(self.pages):
            page_url = self.url + "/page-{}".format(page + 1)
            self.get_property_urls(page_url)
        self.property_urls = list(set(self.property_urls))

    def get_pages(self, url):
        proxy = {"proxy": "http:\\{}".format(random.choice(self.proxy))}
        headers = {'User-Agent': self.ua.random}
        soup = BeautifulSoup(requests.get(url, proxies=proxy, headers=headers).content, "html.parser")
        page = soup.find_all("a", {"class": "clickable goToPage"})[-1].get_text()
        try:
            self.pages = int(page)
        except:
            pass

    def get_property_urls(self, url):
        proxy = {"proxy": "http:\\{}".format(random.choice(self.proxy))}
        headers = {'User-Agent': self.ua.random}
        soup = BeautifulSoup(requests.get(url, proxies=proxy, headers=headers).content, "html.parser")
        links = soup.find_all("a", {"class": "slider-item"})
        for link in links:
            link_text = link["href"]
            self.property_urls.append(link_text)

class Property:
    def __init__(self, url = "", proxy = None):
        if not "https" in url:
            self.url = "https://www.redfin.com{}".format(url)
        else:
            self.url = url
        self.proxy = proxy
        self.ua = UserAgent(verify_ssl=False, use_cache_server=False)
        self.detail = {}

    def get_detail(self):
        pass

if __name__ == "__main__":
    p = Proxy()
    r = Redfin(zip_code="46204", proxy=p.ip_proxies)
    print(r.property_urls)

