import requests
import sys
import time


def export_for_blog_post(books):
    for book in books:
        year, month, day = book["date"].split("-")
        print u'* *{title}*, {author} ({day}/{month})'.format(
                day=day, month=month, **book)


def add_librarything(books, api_key):
    url = 'http://www.librarything.com/services/rest/1.1/'
    for book in books:
        if 'librarything' in book:
            continue
        response = requests.get(
                url, params={'method': 'librarything.ck.getwork',
                             'name': book['title'],
                             'apikey': api_key})
        book['librarything'] = response.content
        time.sleep(2)
        sys.stdout.write('*')
        sys.stdout.flush()
