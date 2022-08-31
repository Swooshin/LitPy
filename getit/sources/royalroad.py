import re
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class RoyalRoad():
    def __init__(self):
        self._url_rr = "https://www.royalroad.com"
        
        self._options = FireFoxOptions()
        # self._options.add_argument("--headless")
        
        self._driver = webdriver.Firefox(options=self._options)

    def getChapterList(self, url_base):
        # Request page
        self._driver.get(url_base)

        # Wait for page to load
        element = WebDriverWait(driver=self._driver, timeout=5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class=portlet-body')))
        
        # Pass page source into Beautiful Soup
        soup = BeautifulSoup(self._driver.page_source)
        # Compile a regex pattern to use to find the list
        pattern = re.compile(r'window\.chapters = (\[.*?\])', re.MULTILINE)
        script = soup.find("script", text=pattern)

        chapter_list = []
        if script:
            match = pattern.search(script.text)
            if match:
                chapter_list = json.loads(match.group(1))
                return chapter_list
        
        return chapter_list

    def getChapterContent(self, chapter_list):
            content = []
            for chapter in chapter_list[0:5]:
                print(f"{self._url_rr}{chapter.get('url')}")
                try:
                    page = requests.get(
                        f"{self._url_rr}{chapter.get('url')}", headers={"User-Agent": "Chrome/47.0.2526.111"}
                    )
                    print("Status 200")
                except Exception:
                    print("Status 404")
                    continue
                soup = BeautifulSoup(page.content, "html.parser")
                page.raise_for_status()

                print(page.status_code)
                result = soup.find("div", class_="chapter-content")
                print(result.contents)


        #         chapterno = chapter_url.split("/")[-1].replace("chapter-", "")

        #         results = soup.find('div', class_='hidden')

        #         try:
        #             chaptername = results.find('h3').get_text()
        #         except AttributeError as err:
        #             print('Chapter-{} {}'.format(i, err))
        #             chaptername = "Chapter {} .".format(chapterno)

        #         paragraphs = results.find_all('p')
        #         paragraphs = paragraphs[:len(paragraphs) - 2]
        #         paragraphs.insert(0, '<h1>Chapter {}</h1>'.format(i))
        #         paragraphs.insert(0, '<html>')
        #         paragraphs.append('</html>')

        #         LNout = {
        #             "name": chapter_url.split("/")[-2].replace("-", " ").title(),
        #             "chapterno": chapterno,
        #             "chaptername": chaptername,
        #             "text": ''.join([str(n) for n in paragraphs])
        #         }

        #         content.append(LNout)

        #     return content

    def getMetaData():
        pass

    def getRejectedTags():
        pass
    


