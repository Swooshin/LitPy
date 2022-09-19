from ebooklib import epub

import logging

logger = logging.getLogger(__name__)


def create_ebook(content, book_id, book_title, book_save):
    book = epub.EpubBook()

    # set metadata
    book.set_identifier(book_id)
    book.set_title(book_title)
    book.set_language("en")

    # Create chapters for book
    chapters = []
    for chapter in content:
        c = epub.EpubHtml(
            title=chapter.title, file_name=f"{chapter.slug}.xhtml", lang="en"
        )
        c.set_content(chapter.content)
        book.add_item(c)
        chapters.append(c)

    style = "body { font-family: Times, Times New Roman, serif; }"

    nav_css = epub.EpubItem(
        uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style
    )
    book.add_item(nav_css)

    book.toc = chapters

    chapters.insert(0, "nav")
    book.spine = chapters

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # write to the file
    epub.write_epub(book_save, book, {})
