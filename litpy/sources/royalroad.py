import re
import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

from model import Chapter


class RoyalRoad:
    def __init__(self):
        self._url_rr = "https://www.royalroad.com"

        self._options = FireFoxOptions()
        # self._optionss.add_argument("--headless")
        try:
            self._driver = webdriver.Firefox(options=self._options)
        except WebDriverException:
            self._driver = None

    def get_chapter_list(self, url_lit):
        # Request page
        self._driver.get(url_lit)

        # Wait for page to load
        element = WebDriverWait(driver=self._driver, timeout=5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class=portlet-body"))
        )

        # Pass page source into Beautiful Soup
        soup = BeautifulSoup(self._driver.page_source, "html.parser")
        # Compile a regex pattern to use to find the list
        pattern = re.compile(r"window\.chapters = (\[.*?\])", re.MULTILINE)
        script = soup.find("script", text=pattern)

        chapter_list = []
        if script:
            match = pattern.search(script.text)
            if match:
                data = json.loads(match.group(1))
                for d in data:
                    chapter_list.append(
                        Chapter(
                            d.get("title"),
                            d.get("slug"),
                            d.get("order"),
                            0,
                            d.get("url"),
                            "",
                        )
                    )
                return chapter_list
        return chapter_list

    def get_chapter_content(
        self, chapter_list, start_chapter=None, end_chapter=None, delay=2
    ):
        if chapter_list is None:
            return

        if start_chapter is None:
            start_chapter = 0
        elif start_chapter == 0:
            start_chapter = 0
        else:
            start_chapter = start_chapter - 1

        if end_chapter is None:
            end_chapter = len(chapter_list)

        chapter_list = chapter_list[start_chapter:end_chapter]

        content = []
        for chapter in chapter_list:
            tmp_dict = {}
            tmp_dict = chapter
            try:
                page = requests.get(
                    f"{self._url_rr}{chapter.url}",
                    headers={"User-Agent": "Chrome/47.0.2526.111"},
                )
                print("Status 200")
            except Exception:
                print("Status 404")
                continue
            soup = BeautifulSoup(page.content, "html.parser")
            page.raise_for_status()

            result = "".join(
                map(str, soup.find("div", class_="chapter-content").contents)
            )
            chapter.updateContent(result)

            time.sleep(delay)

        return chapter_list

    def pull_data(self, url_lit, start_chapter=None, end_chapter=None, delay=2):
        chapter_list = self.get_chapter_list(url_lit)
        content = self.get_chapter_content(
            chapter_list, start_chapter=start_chapter, end_chapter=end_chapter
        )
        return content

    def get_meta_data():
        pass

    def get_rejected_tags():
        pass
