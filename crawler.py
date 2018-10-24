from bs4 import BeautifulSoup
import re
import os
import sys
import requests
from urllib.parse import urljoin


def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s


def get_page(page):
    try:
        content = requests.get(page, timeout=1).text
    except Exception as e:
        print(e)
        content = ''
    return content


def get_all_links(content, url):
    soup = BeautifulSoup(content, 'html5lib')
    full_links = {a['href'] for a in soup.find_all(
        'a', href=re.compile(r'^http'))}
    # Construct full URLs from relative paths
    relative_links = {urljoin(url, a['href'])for a in soup.find_all(
        'a', href=re.compile(r'^/'))}
    return full_links | relative_links


def union_dfs(a, b):
    for e in b:
        if e not in a:
            a.append(e)


def union_bfs(a, b):
    unique_for_a = b - set(a)
    for x in unique_for_a:
        a.insert(0, x)


def add_page_to_folder(url, content):
    """
    将网页存到文件夹里，将网址和对应的文件名写入index.txt中

    :param url:
    :param content:
    :return:
    """
    index_filename = 'index.txt'    # index.txt中每行是'网址 对应的文件名'
    folder = 'html'                 # 存放网页的文件夹
    filename = valid_filename(url)  # 将网址变成合法的文件名
    with open(index_filename, 'a') as f_index:
        f_index.write(url + '\t' + filename + '\n')
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    with open(os.path.join(folder, filename), 'w') as f:
        f.write(content)            # 将网页存入文件


def crawl(seed, method, max_page):
    tocrawl = [seed]
    crawled = []
    graph = {}
    count = 0
    
    while tocrawl and count < max_page:
        url = tocrawl.pop()
        if url not in crawled:
            count += 1
            crawled.append(url)
            print(url)
            content = get_page(url)
            add_page_to_folder(url, content)
            outlinks = get_all_links(content, url)
            if len(outlinks):
                graph[url] = outlinks
            globals()['union_' + method](tocrawl, outlinks)
    return graph, crawled


if __name__ == '__main__':
    seed = sys.argv[1]
    method = sys.argv[2]
    max_page = sys.argv[3]
    
    graph, crawled = crawl(seed, method, int(max_page))
