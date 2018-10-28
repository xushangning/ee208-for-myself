import sqlite3
import threading
from queue import Queue
import urllib.parse
from time import time

import requests
from bs4 import BeautifulSoup

from GeneralHashFunctions import *
from bloomfilter import BloomFilter


class CrawledDoc:
    def __init__(self, url=''):
        self.src = ''
        self.url = url


class CrawlerThread(threading.Thread):
    pages_count = 0
    max_pages = 40000
    queue = Queue()
    filter = BloomFilter(1048576, False, RSHash, hash, JSHash, SDBMHash, FNVHash)
    lock = threading.Lock()
    valid_char_in_filename = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()
        self.doc = CrawledDoc()
        super().__init__()

    def run(self):
        cls = self.__class__
        while cls.pages_count < cls.max_pages:
            self.doc = CrawledDoc(cls.queue.get())
            cls.queue.task_done()
            if ('duokan' in self.doc.url
                    and not self.filter.query(self.doc.url)
                    and self.is_html()):
                try:
                    r = requests.get(self.doc.url, timeout=1)
                    r.raise_for_status()

                    # Falling back to ISO-8859-1 if no encoding is specified
                    # is a pretty bad idea. Let Beautiful Soup determine
                    # encoding from <meta> instead.
                    if 'charset' not in r.headers['Content-Type']:
                        soup = BeautifulSoup(r.content, 'html5lib')
                    else:
                        soup = BeautifulSoup(r.text, 'html5lib')

                    try:
                        title = soup.find('title').string.strip()
                    except AttributeError:
                        title = self.doc.url
                        print(self.name + ': ' + self.doc.url)
                        print('    AttributeError: the webpage doesn\'t have a title')

                    cls.lock.acquire()
                    self.filter.set(self.doc.url)
                    for img in soup.find_all('img', src=True, alt=True):
                        cls.pages_count += 1
                        print(self.name + ':', cls.pages_count, img['src'])
                        self.cursor.execute(
                            'INSERT INTO indices VALUES (?, ?, ?, ?)',
                            (img['src'], img['alt'], title, int(time()))
                        )
                    db.commit()
                    # add URLs in the web page to the queue
                    # Duplicate URLs are not removed in this stage.
                    for a in soup.find_all('a', href=True):
                        link = a['href'].rstrip('javascript:void(0)')
                        if link.startswith('http'):
                            cls.queue.put(link)
                        elif link.startswith('/'):     # absolute path
                            cls.queue.put(urllib.parse.urljoin(
                                self.doc.url, link))
                        elif len(link):                # relative path
                            if not self.doc.url.endswith('/'):
                                link = '/' + link
                            cls.queue.put(self.doc.url + link)
                    cls.lock.release()

                # handle exceptions in request and bad responses
                except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
                    print(self.name + ': ' + self.doc.url + '\n   ', e)
        self.db.close()

    def is_html(self):
        try:
            r = requests.head(self.doc.url, timeout=1)
            return 'text/html' in r.headers.get('Content-Type', '')
        except requests.exceptions.RequestException as e:
            print(self.name + ': ' + self.doc.url + '\n   ', e)
            return False

    def url2filename(self):
        return ''.join(c for c in self.doc.url if c in self.__class__.valid_char_in_filename)[:64]


if __name__ == '__main__':
    CrawlerThread.queue.put('https://www.duokan.com')
    thread_pool = []
    N_THREADS = 1
    IMAGES_INDEX_PATH = 'index/images/image_index.sqlite'
    # Disable checking for multiple threads sharing one connection as we try to
    # synchronize writes with the variable lock.
    db = sqlite3.connect(IMAGES_INDEX_PATH, check_same_thread=False)
    main_cursor = db.cursor()

    main_cursor.execute('CREATE TABLE IF NOT EXISTS indices ('
                        'url TEXT NOT NULL,'
                        'description TEXT,'
                        'title TEXT,'
                        'updated_at INTEGER NOT NULL)')

    for _ in range(N_THREADS):
        t = CrawlerThread(db)
        t.start()
        thread_pool.append(t)
    for t in thread_pool:
        t.join()
    db.close()
