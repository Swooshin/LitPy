from getit.sources.royalroad import RoyalRoad
from builder.builder import createEbook

if __name__ == "__main__":
    url_base = "https://www.royalroad.com/fiction/21220/mother-of-learning"
    test_dump = [{"id":301778,"volumeId":"null","title":"1. Good Morning  Brother","slug":"1-good-morning-brother","date":"2018-10-28T21:34:43Z","order":0,"visible":1,"url":"/fiction/21220/mother-of-learning/chapter/301778/1-good-morning-brother"},{"id":301781,"volumeId":"null","title":"2. Life\u2019s Little Problems","slug":"2-lifes-little-problems","date":"2018-10-28T21:45:44Z","order":1,"visible":1,"url":"/fiction/21220/mother-of-learning/chapter/301781/2-lifes-little-problems"},{"id":301784,"volumeId":"null","title":"3. The Bitter Truth","slug":"3-the-bitter-truth","date":"2018-10-28T21:53:10Z","order":2,"visible":1,"url":"/fiction/21220/mother-of-learning/chapter/301784/3-the-bitter-truth"},{"id":301788,"volumeId":"null","title":"4. Stars Fell","slug":"4-stars-fell","date":"2018-10-28T21:59:44Z","order":3,"visible":1,"url":"/fiction/21220/mother-of-learning/chapter/301788/4-stars-fell"},{"id":301795,"volumeId":"null","title":"5. Start Over","slug":"5-start-over","date":"2018-10-28T22:07:23Z","order":4,"visible":1,"url":"/fiction/21220/mother-of-learning/chapter/301795/5-start-over"}]
    royalroad = RoyalRoad()
    # chapter_list = royalroad.getChapterList(url_base)
    content = royalroad.getChapterContent(test_dump)

    createEbook(content)