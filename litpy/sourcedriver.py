import re
from sources.royalroad import RoyalRoad


def SourceDriver(url_lit):
    if re.search("royalroad.com", url_lit):
        sourcedriver = RoyalRoad()
    else:
        sourcedriver = None

    return sourcedriver
