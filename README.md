# About Litpy
LitPy is a Python library for scraping webnovels from popular websites and converting them to an EPUB format.

The functionality is inteded to be very simplistic.

This is a side project and likely will not be maintained well.

# Sample
``` python
import LitPy

litpy = LitPy()
options = {
    "url_lit": "URL_TO_NOVEL",
    "start_chapter": 1,
    "end_chapter": 20,
    "delay": 10,
    "book_id": "CUSTOM_BOOK_ID_FOR_NOVEL",
    "book_title": "CUSTOM_BOOK_TITLE_FOR_NOVEL",
    "book_save": "SAVE_FILE_PATH.epub",
}
litpy.set_options(options)

litpy.convert2epub()

```

# Licence
LitPy is licenced under the AGPL licence.