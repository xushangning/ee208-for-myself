import threading
from queue import Queue

from bloomfilter import BloomFilter
import crawler
from GeneralHashFunctions import *

seed = 'https://www.sjtu.edu.cn'
q = Queue()
max_page = 2000
count_pages = 0
graph = {}

BIT_ARRAY_SIZE = 16384
my_filter = BloomFilter(BIT_ARRAY_SIZE, hash, RSHash, JSHash, SDBMHash, FNVHash)

N_THREADS = 4
var_lock = threading.Lock()


def crawling():
    global count_pages
    while count_pages < max_page:
        print(count_pages, end=' ')
        url = q.get()
        if not my_filter.query(url):
            print(url)
            content = crawler.get_page(url)
            if len(content):
                my_filter.set(url)
                crawler.add_page_to_folder(url, content)
                outlinks = crawler.get_all_links(content, url)
                var_lock.acquire()  # ready to change the global environment
                count_pages += 1
                if len(outlinks):
                    graph[url] = outlinks
                    for link in outlinks:
                        q.put(link)
                var_lock.release()
        q.task_done()


q.put(seed)
thread_pool = []
for _ in range(N_THREADS):
    t = threading.Thread(target=crawling)
    t.start()
    thread_pool.append(t)
for t in thread_pool:
    t.join()

my_filter.print_stats()
print("Number of Crawled Pages:", count_pages)
