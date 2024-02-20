from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service;
from webdriver_manager.chrome import ChromeDriverManager;
from datetime import datetime

class scraperClass:
    articles = []
    def scraper(self, source):
        scraper = self._get_scraper(source["source"])
        scraper(source)
        return self.articles
    
    
    def _get_scraper(self, source):
        match source:
            case "hespress":
                return self._hespressScraper
            case "hibapress":
                return self._hibapressScraper
            case "hespressEnglish":
                return self._hespressEnglishScraper
            case "lnt":
                return self._lntScraper
            case _:
                raise ValueError(source)
    def _hespressScraper(self, source):
        response = requests.get(source["link"]).text
        soup = BeautifulSoup(response, "lxml")
        data = soup.findAll("div", {'class': "carousel-item"})
        for i, row in enumerate(data):
            if i == 0 or i == len(data) - 1:
                continue
            link_tag = row.find("a")
            title = link_tag.get_text()
            link = link_tag.get("href")
            img = row.find("img").get("src")
            article = {
                'id': title,
                'link': link,
                'img': img,
                'source': source["source"],
                'created_at': datetime.now().isoformat()  
            }
            self.articles.append(article)
        return True
    
    def _hibapressScraper(self, source):
        response = requests.get(source["link"]).text
        soup = BeautifulSoup(response, "lxml")
        data = soup.findAll("li", {'class': 'post-item'})
        for row in data:
            img = row.find("img")
            link_tag = row.find("a")
            link = link_tag.get("href")
            title = link_tag.get("aria-label")
            if img != None :
                src = img.get("src") 
            else :
                src = None
            article = {
                'id': title,
                'link': link,
                'img': src,
                'source': source["source"],
                'created_at': datetime.now().isoformat()    
            }    
            self.articles.append(article)
        return True
    
    def _hespressEnglishScraper(self, source):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(source["link"])
        time.sleep(7)
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        html = driver.page_source

        # Parse the HTML code using BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        data = soup.findAll("div", {'class': "carousel-item"})  
        for i, row in enumerate(data):
            if i == 0 or i == len(data) - 1:
                continue
            link_tag = row.find("a")
            title = link_tag.get_text()
            link = link_tag.get("href")
            img = row.find("img").get("src")
            article = {
                'id': title,
                'link': link,
                'img': img,
                'source': source["source"],
                'created_at': datetime.now().isoformat()    
            }  
            self.articles.append(article)
        return True
    
    def _lntScraper(self, source):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(source["link"])
        # Wait for the page to load
        time.sleep(15)
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        data = soup.findAll("article", {'class': 'c-card'})
        for row in data:
            if row['class'][0] == "skeleton":
                continue
            else:
                link_tag = row.find("a")
                link = link_tag.get("href")
                img = row.find("img").get("src")
                title = row.find("h2").find("a").get_text()
                article = {
                    'id': title,
                    'link': link,
                    'img': img,
                    'source': "LNT",
                    'created_at': datetime.now().isoformat()   
                } 
                self.articles.append(article)
        return True
    
