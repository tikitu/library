import bs4
import json
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


def write_file(books, filename):
    json.dump(books, open(filename, 'w'), indent=1, sort_keys=True)


def check_matches(books, callback):
    for book in books:
        soup = bs4.BeautifulSoup(book['librarything'], 'html.parser')
        author = soup.find('author')
        title = soup.find('title')
        if not author or not title:
            continue
        author = author.text
        title = title.text
        if author == book['author'] and title == book['title']:
            match = True
        else:
            print u'Tikitu: {title} -- {author}'.format(**book)
            print u'LT    : {title} -- {author}'.format(
                    title=title, author=author)
            match = raw_input('[y/N]') == 'y'
        callback(book, soup, matches=match)


def extract_url_from_lt(books):
    def set_url(book, soup, matches):
        if 'url' in book:
            return
        if matches:
            url = soup.find('url')
            if url:
                book['url'] = url
    check_matches(books, set_url)


def remove_erroneous_lt_data(books):
    def clean_book(book, _soup, matches):
        if not matches:
            del book['librarything']
    check_matches(books, clean_book)