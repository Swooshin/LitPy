from ebooklib import epub

def createEbook(content):
    book = epub.EpubBook()

    # set metadata
    book.set_identifier('Sample')
    book.set_title('Sample')
    book.set_language('en')

    # Create chapters for book
    chapters = []
    for chapter in content:
        print(chapter['title'], chapter['slug'], chapter['content'])
        c = epub.EpubHtml(
            title = chapter['title'],
            file_name=f"{chapter['slug']}.xhtml",
            lang='en'
        )
        c.set_content(chapter['content'])
        book.add_item(c)
        chapters.append(c)

    # Create style format
    style = 'body { font-family: Times, Times New Roman, serif; }'

    # Create navigation at start
    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content=style
    )
    book.add_item(nav_css)

    # Set table of contents
    book.toc = chapters
    chapters.insert(0, 'nav')
    book.spine = chapters

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub("Sample.epub", book)