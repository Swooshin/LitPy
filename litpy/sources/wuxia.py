import time
import json
import re


from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

from model import Chapter


class Wuxia:
    def __init__(self, webdriver):
        self._url = "https://www.wuxiaworld.com"
        self._driver = webdriver

    def get_chapter_list(self, url_lit):
        self._driver.get(url_lit)

        # Wait for page to load
        element = WebDriverWait(driver=self._driver, timeout=5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[id=full-width-tab-1")
            )
        )

        self._driver.find_element(By.CSS_SELECTOR, "button[id=full-width-tab-1").click()

        self._driver.find_elements(
            By.CSS_SELECTOR,
            "div.MuiButtonBase-root.MuiAccordionSummary-root.border-b.border-solid",
        )[1].click()

        element = WebDriverWait(driver=self._driver, timeout=5).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "a.group[data-amplitude-click-event='ChapterEvents.ClickChapter']",
                )
            )
        )

        # Pass page source into Beautiful Soup
        soup = BeautifulSoup(self._driver.page_source, "html.parser")

        link_containers = soup.find_all(
            "div", class_=re.compile("^border-b border-gray-300 dark:border-gray-800.*")
        )

        chapter_list = []
        for container in link_containers:
            link = container.find("a")
            params = json.loads(link["data-amplitude-params"])

            chapter_list.append(
                Chapter(
                    params["chapterTitle"],
                    params["chapterTitle"],
                    0,
                    params["chapterNo"],
                    link["href"],
                    "",
                )
            )

        return chapter_list

    def get_chapter_content(
        self, chapter_list, start_chapter=None, end_chapter=None, delay=2
    ):
        if chapter_list is None:
            return None

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
            print(f"{self._url}{chapter.url}")
            try:
                page = requests.get(
                    f"{self._url}{chapter.url}",
                    headers={"User-Agent": "Chrome/47.0.2526.111"},
                )
                print("Status 200")
            except Exception:
                print("Status 404")
                continue

            soup = BeautifulSoup(page.content, "html.parser")
            page.raise_for_status()

            print(soup)

            # result = "".join(
            #     map(str, soup.find("div", class_="chapter-content").contents)
            # )
            # chapter.updateContent(result)

            # time.sleep(delay)

        return chapter_list

    def pull_data(self, url_lit, start_chapter=None, end_chapter=None, delay=2):
        chapter_list = self.get_chapter_list(url_lit)
        content = self.get_chapter_content(
            chapter_list, start_chapter=start_chapter, end_chapter=end_chapter
        )
        return content
