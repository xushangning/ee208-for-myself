import os
import threading
from queue import Queue
import urllib.parse

import requests
from bs4 import BeautifulSoup

from GeneralHashFunctions import *
from bloomfilter import BloomFilter


class CrawledDoc:
    def __init__(self, url=''):
        self.text = ''
        self.url = url


class CrawlerThread(threading.Thread):
    pages_count = 0
    max_pages = 10000
    queue = Queue()
    filter = BloomFilter(1048576, False, RSHash, hash, JSHash, SDBMHash, FNVHash)
    lock = threading.Lock()
    valid_char_in_filename = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    def __init__(self, index_file):
        self.index_file = index_file
        self.doc = CrawledDoc()
        super().__init__()

    def run(self):
        cls = self.__class__
        while cls.pages_count < cls.max_pages:
            self.doc = CrawledDoc(cls.queue.get())
            cls.queue.task_done()
            if ('sjtu' in self.doc.url
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

                    for tag in soup.find_all(['script', 'style']):
                        tag.decompose()
                    try:
                        # detect parsing errors after <script> and <style>
                        # were removed
                        repr(soup)
                    except RecursionError as e:
                        print(self.name + ': ' + self.doc.url + '\n   ', e)
                        continue

                    self.doc.text = soup.get_text('\n', strip=True)
                    if len(self.doc.text):
                        self.filter.set(self.doc.url)
                        print(self.name + ':', cls.pages_count, self.doc.url)
                        try:
                            title = soup.find('title').string.strip()
                        except AttributeError:
                            title = self.doc.url
                            print(self.name + ': ' + self.doc.url)
                            print('    AttributeError: the webpage doesn\'t have a title')

                        filename = self.url2filename()
                        with open('crawled/html/' + filename, 'w') as f:
                            f.write(str(soup))
                        with open('crawled/text/' + filename, 'w') as f:
                            f.write(self.doc.text)

                        cls.lock.acquire()
                        self.index_file.write(self.doc.url
                                              + '\t' + filename
                                              + '\t' + title + '\n')

                        # add URLs in the web page to the queue
                        # Duplicate URLs are not removed in this stage.
                        for a in soup.find_all('a', href=True):
                            link = ''.join(c for c in a['href'] if not c.isspace())
                            if link.startswith('http'):
                                cls.queue.put(link)
                            elif link.startswith('/'):     # absolute path
                                cls.queue.put(urllib.parse.urljoin(
                                    self.doc.url, link))
                            elif len(link):                # relative path
                                if not self.doc.url.endswith('/'):
                                    link = '/' + link
                                cls.queue.put(self.doc.url + link)
                        cls.pages_count += 1
                        cls.lock.release()

                # handle exceptions in request and bad responses
                except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
                    print(self.name + ': ' + self.doc.url + '\n   ', e)

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
    if not os.path.exists('crawled/html'):
        os.mkdir('crawled/html')
    if not os.path.exists('crawled/text'):
        os.mkdir('crawled/text')
    CrawlerThread.queue.put('https://www.sjtu.edu.cn')
    thread_pool = []
    N_THREADS = 1
    index_file = open('crawled/index.txt', 'w')

    for _ in range(N_THREADS):
        t = CrawlerThread(index_file)
        t.start()
        thread_pool.append(t)
