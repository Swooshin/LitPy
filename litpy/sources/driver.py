import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.common.exceptions import WebDriverException


from sources.royalroad import RoyalRoad

import logging

logger = logging.getLogger(__name__)


def SourceDriver(url_lit):
    if re.search("royalroad.com", url_lit):
        sourcedriver = RoyalRoad(get_driver())
    else:
        sourcedriver = None

    return sourcedriver


def get_driver():
    options = FireFoxOptions()

    try:
        driver = webdriver.Firefox(options=options)
    except WebDriverException:
        driver = None

    return driver
