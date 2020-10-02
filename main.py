import requests
from bs4 import BeautifulSoup
from ebooklib import epub


def LNIgnoreList():
    ignore_list = [
        '''<p>If you find any errors ( broken links, non-standard content, etc . . ), Please let us know so we can fix it as soon as possible . </p>''',
        '''<p>Tip: You can use left, right, A and D keyboard keys to browse between chapters .</p>'''
    ]
    return ignore_list


def LNGetSingle(URL):
    URL = 'https://www.readlightnovel.org/the-second-coming-of-gluttony/chapter-1'
    page = requests.get(URL, headers={"User-Agent": "Chrome/47.0.2526.111"})

    print(page.status_code)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find('div', class_='hidden')
    paragraphs = results.find_all('p')

    for n in LNIgnoreList():
        paragraphs.remove(n)

    # paragraphs = paragraphs[:len(paragraphs) - 2]
    paragraphs.insert(0, '<html>')
    paragraphs.append('</html>')

    LNout = {
        "name": URL.split("/")[-2].replace("-", " "),
        "chapter": URL.split("/")[-1].replace("chapter-", ""),
        "text": ''.join([str(n) for n in paragraphs])
    }

    return LNout


def LNGetMultiple(URL, chapter_req):
    content = []
    for i in range(chapter_req[0], chapter_req[1] + 1):
        chapter_url = '{}/chapter-{}'.format(URL, i)
        try:
            page = requests.get(chapter_url, headers={"User-Agent": "Chrome/47.0.2526.111"})

            soup = BeautifulSoup(page.content, 'html.parser')
            page.raise_for_status()

            if soup.find('title').text == '404 Not Found':
                raise TypeError

            print('Chapter-{} Status {}'.format(i, page.status_code))
        except Exception:
            print('Chapter-{} Status 404'.format(i))
            continue

        chapterno = chapter_url.split("/")[-1].replace("chapter-", "")

        results = soup.find('div', class_='hidden')

        try:
            chaptername = results.find('h3').get_text()
        except AttributeError as err:
            print('Chapter-{} {}'.format(i, err))
            chaptername = "Chapter {} .".format(chapterno)

        paragraphs = results.find_all('p')
        paragraphs = paragraphs[:len(paragraphs) - 2]
        paragraphs.insert(0, '<h1>Chapter {}</h1>'.format(i))
        paragraphs.insert(0, '<html>')
        paragraphs.append('</html>')

        LNout = {
            "name": chapter_url.split("/")[-2].replace("-", " ").title(),
            "chapterno": chapterno,
            "chaptername": chaptername,
            "text": ''.join([str(n) for n in paragraphs])
        }

        content.append(LNout)

    return content


def EpubCreateSingle(content):
    book = epub.EpubBook()

    # set metadata
    book.set_identifier('Test123')
    book.set_title("%s - Chapter %s" % (content['name'], content['chapter']))
    book.set_language('en')

    # create Chapter
    c1 = epub.EpubHtml(
        title="Chapter %s" % content['chapter'],
        file_name=content['chapter'],
        lang='en'
    )
    c1.set_content(content['text'])

    book.add_item(c1)

    style = 'body { font-family: Times, Times New Roman, serif; }'

    nav_css = epub.EpubItem(uid="style_nav",
                            file_name="style/nav.css",
                            media_type="text/css",
                            content=style)
    book.add_item(nav_css)

    book.spine = ['nav', c1]

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub('test.epub', book)


def EpubCreateMultiple(content, coverimg):
    book = epub.EpubBook()

    # set metadata
    book.set_identifier('Chrysalis-1-{}'.format(content[-1]['chapterno']))
    book.set_title('{} Chapter {}-{}'.format(content[0]['name'], content[0]['chapterno'], content[-1]['chapterno']))
    book.set_language('en')

    if coverimg is True:
        book.set_cover('cover.jpg', open('cover.jpg', 'rb').read())

    chapters = []
    for chapter in content:
        c = epub.EpubHtml(
            title=chapter['chaptername'],
            file_name="{}.xhtml".format(chapter['chapterno']),
            lang='en'
        )
        c.set_content(chapter['text'])
        book.add_item(c)
        chapters.append(c)

    style = 'body { font-family: Times, Times New Roman, serif; }'

    nav_css = epub.EpubItem(uid="style_nav",
                            file_name="style/nav.css",
                            media_type="text/css",
                            content=style)
    book.add_item(nav_css)

    book.toc = chapters

    chapters.insert(0, 'nav')
    book.spine = chapters

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub('{} Chapter {}-{}.epub'.format(content[0]['name'], content[0]['chapterno'], content[-1]['chapterno']), book)


def GetCover(URL):
    try:
        page = requests.get(URL, headers={"User-Agent": "Chrome/47.0.2526.111"})
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find('div', class_='novel-cover')
        coversrc = results.find('img').get('src')
        coverimg = requests.get(coversrc)
        with open('cover.jpg', 'wb') as file:
            file.write(coverimg.content)
        return True
    except:
        return False


def main():
    URL = 'https://www.readlightnovel.org/chrysalis'
    chapter_req = (1, 1)

    coverimg = GetCover(URL)
    content = LNGetMultiple(URL, chapter_req)
    print(content[0]['name'])
    EpubCreateMultiple(content, coverimg)


if __name__ == '__main__':
    main()
