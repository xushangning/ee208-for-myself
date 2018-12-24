import os
import sqlite3
import threading
from queue import Queue
import urllib.parse
from time import gmtime, strftime

import requests
from bs4 import BeautifulSoup

from GeneralHashFunctions import *
from bloomfilter import BloomFilter


class CrawledDoc:
    """A simple class that stores a crawled webpage"""
    def __init__(self, url=''):
        self.text = ''
        self.url = url


class CrawlerThread(threading.Thread):
    """A multi-thread crawler"""
    pages_count = 0     # count the number of webpages crawled
    max_pages = 10000   # the target number of webpages to crawl
    queue = Queue()     # the job queue shared among all threads
    webpage_url_filter = BloomFilter(1048576, False, RSHash, hash, JSHash,
                                     SDBMHash, FNVHash)
    image_url_filter = BloomFilter(4194304, False, RSHash, hash, JSHash,
                                   SDBMHash, FNVHash)
    lock = threading.Lock()
    # characters valid for use in file name, adapted from
    # valid_filename() in crawler.py
    valid_char_in_filename = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    def __init__(self, webpage_db, image_db, table_name):
        """
        :param webpage_db: database for webpages
        :param image_db: database for images
        :param table_name: the table name to operate on
        """
        self.webpage_db = webpage_db
        self.webpage_db_cursor = webpage_db.cursor()
        self.image_db = image_db
        self.image_db_cursor = image_db.cursor()
        self.table_name = table_name
        self.doc = CrawledDoc()     # represent the webpage being crawled
        super().__init__()          # call the super constructor

    def run(self):
        cls = self.__class__        # sugar for accessing parent class
        while cls.pages_count < cls.max_pages:
            # retrieve a URL from the job queue and initialized a CrawledDoc
            self.doc = CrawledDoc(cls.queue.get())
            # Mark as done immediately because the crawler won't return to the
            cls.queue.task_done()                                   # same URL.
            if ('sjtu' in self.doc.url  # restrict to SJTU sites
                    # query the Bloom filter
                    and not self.webpage_url_filter.query(self.doc.url)
                    and self.is_html()):    # check the Content-Type header
                try:    # for catching request exceptions and HTTP errors
                    r = requests.get(self.doc.url, timeout=1)
                    r.raise_for_status()    # raise HTTP errors as exception

                    # The Requests module will automatically inspect the
                    # Content-Type header for encoding. If no encoding is
                    # specified, it will fall back to ISO-8859-1, per the
                    # requirement of RFC 2616, which can't be a worse idea.
                    # Pass binary data to Beautiful Soup to let it determine
                    # encoding from <meta> instead.
                    if 'charset' not in r.headers['Content-Type']:
                        soup = BeautifulSoup(r.content, 'html5lib')
                    else:
                        soup = BeautifulSoup(r.text, 'html5lib')

                    # strip the HTML of <script> and <style>, or they will be
                    # returned by get_text()
                    for tag in soup.find_all(['script', 'style']):
                        tag.decompose()
                    try:
                        # detect parsing errors after <script> and <style>
                        # were removed
                        repr(soup)
                    except RecursionError as e:
                        print(self.name + ': ' + self.doc.url + '\n   ', e)
                        continue

                    # get all the texts, stripped, separated by newline
                    self.doc.text = soup.get_text('\n', strip=True)
                    if len(self.doc.text):
                        # mark as crawled only if it has meaningful texts
                        self.webpage_url_filter.set(self.doc.url)
                        # output on successfully crawling a web page
                        print(self.name + ':', cls.pages_count, self.doc.url)
                        try:
                            # try to extract the title
                            title = soup.find('title').string.strip()
                        except AttributeError:
                            title = self.doc.url    # use its URL as title
                            print(self.name + ': ' + self.doc.url)
                            print('    AttributeError: the webpage doesn\'t have a title')

                        # convert a URL to a valid filename
                        filename = self.url2filename()
                        # write webpage source
                        with open('crawled/html/' + filename, 'w') as f:
                            f.write(str(soup))
                        # write texts
                        with open('crawled/text/' + filename, 'w') as f:
                            f.write(self.doc.text)

                        cls.lock.acquire()
                        # writing to the webpage database
                        self.webpage_db_cursor.execute(
                            'INSERT INTO {} VALUES (?, ?, ?)'.format(table_name),
                            (self.doc.url, title, filename)
                        )
                        self.webpage_db.commit()

                        # find all <img> with src and alt attributes
                        for img in soup.find_all('img', src=True, alt=True):
                            if len(img['src']):
                                img_url = self.construct_url(img['src'])
                                if (not self.image_url_filter.query(img_url)
                                        and len(img['alt'])):
                                    # add image URL to the Bloom filter
                                    self.image_url_filter.set(img_url)
                                    # insert the image URL, its description and its
                                    # origin into the database
                                    self.image_db_cursor.execute(
                                        'INSERT INTO {} VALUES (?, ?, ?)'.format(table_name),
                                        (img_url, img['alt'], self.doc.url)
                                    )
                        self.image_db.commit()

                        # add URLs in the web page to the queue
                        # Duplicate URLs are not removed in this stage.
                        for a in soup.find_all('a', href=True):
                            if len(a['href']):
                                cls.queue.put(self.construct_url(a['href']))
                        # increment the count after everything has been done
                        cls.pages_count += 1
                        cls.lock.release()

                # handle exceptions in request and bad responses
                except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
                    print(self.name + ': ' + self.doc.url + '\n   ', e)

    def is_html(self):
        """Check whether the URL stored in self.doc points to an HTML."""
        try:
            r = requests.head(self.doc.url, timeout=1)  # HEAD instead of GET
            return 'text/html' in r.headers.get('Content-Type', '')
        # handle exceptions during request
        except requests.exceptions.RequestException as e:
            print(self.name + ': ' + self.doc.url + '\n   ', e)
            return False

    def url2filename(self):
        """
        Construct a valid filename from self.doc.url, adapted from
        valid_filename() of crawler.py
        """
        return ''.join(c for c in self.doc.url if c in self.__class__.valid_char_in_filename)[:64]

    def construct_url(self, url):
        """
        Construct URLs from the value of attributes like href of <a> or src of
        <img>. This function models after browsers' behaviour.
        :param url: str, the URL to process
        :return: str
        """
        url = ''.join(c for c in url if not c.isspace())  # remove all spaces
        if url.startswith('http'):     # full URL
            return url
        elif url[0] == '/':            # absolute path
            return urllib.parse.urljoin(self.doc.url, url)
        else:                           # relative path
            if not self.doc.url[-1] == '/':
                url = '/' + url
            return self.doc.url + url


if __name__ == '__main__':
    if not os.path.exists('crawled/html'):
        os.mkdir('crawled/html')
    if not os.path.exists('crawled/text'):
        os.mkdir('crawled/text')
    CrawlerThread.queue.put('https://www.sjtu.edu.cn')  # put in the seed
    thread_pool = []
    N_THREADS = 4

    # Disable checking for multiple threads sharing one connection as we try to
    # synchronize writes with the variable lock.
    webpage_db = sqlite3.connect('crawled/webpage_list.sqlite',
                                 check_same_thread=False)
    image_db = sqlite3.connect('crawled/image_list.sqlite', check_same_thread=False)

    # the table name corresponds to the table creation time
    # like at_20181101_085215
    table_name = strftime('at_%Y%m%d_%H%M%S', gmtime())
    main_cursor = webpage_db.cursor()
    main_cursor.execute('CREATE TABLE IF NOT EXISTS {} ('
                        'url TEXT NOT NULL,'
                        'title TEXT,'
                        'filename TEXT NOT NULL)'.format(table_name))
    main_cursor = image_db.cursor()
    main_cursor.execute('CREATE TABLE IF NOT EXISTS {} ('
                        'url TEXT NOT NULL,'
                        'description TEXT,'
                        'origin TEXT)'.format(table_name))

    for _ in range(N_THREADS):
        t = CrawlerThread(webpage_db, image_db, table_name)
        t.start()
        thread_pool.append(t)
    for t in thread_pool:
        t.join()
    webpage_db.close()
    image_db.close()
