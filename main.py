from getit.sources.royalroad import RoyalRoad

if __name__ == "__main__":
    url_base = "https://www.royalroad.com/fiction/21220/mother-of-learning"
    
    royalroad = RoyalRoad()
    chapter_list = royalroad.getChapterList(url_base)
    royalroad.getChapterContent(chapter_list)