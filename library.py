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


def extract_url_from_lt(books):
    for book in books:
        if 'url' in book:
            continue
        soup = bs4.BeautifulSoup(book['librarything'], 'html.parser')
        author = soup.find('author')
        title = soup.find('title')
        url = soup.find('url')
        if not author or not title or not url:
            continue
        author = author.text
        title = title.text
        url = url.text
        if author == book['author'] and title == book['title']:
            match = True
        else:
            print u'Tikitu: {title} -- {author}'.format(**book)
            print u'LT    : {title} -- {author}'.format(
                    title=title, author=author)
            print u'url   : {url}'.format(url=url)
            match = raw_input('[y/N]') == 'y'
        if match:
            book['url'] = url