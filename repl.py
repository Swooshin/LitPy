import requests
from bs4 import BeautifulSoup
from ebooklib import epub


# def GetUrls(base_url, start_chap, end_chap):
# url_list = []
# initialise selenium and use to retrieve the hyperlinks for all chapters
# for i in range(start_chap, end_chap):
# if i in url_list:
# url_list.append(i)
# continue
# return url_list


def GetContent(url_list):
    content = []
    for chapter_url in url_list:
        try:
            page = requests.get(
                chapter_url, headers={"User-Agent": "Chrome/47.0.2526.111"}
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


def main():
    url_list = [
        "https://www.royalroad.com/fiction/21220/mother-of-learning/chapter/305877/22-complications"
    ]
    GetContent(url_list)


if __name__ == "__main__":
    main()
