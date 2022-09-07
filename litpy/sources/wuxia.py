class Wuxia:
    def __init__(self, webdriver):
        self._url = "https://www.wuxiaworld.com"
        self._driver = webdriver

    def get_chapter_list(self, url_lit):
        self._driver.get(url_lit)
