# 001-(2018-2019-1)EE208

## Directory Structure

Running `parallel_crawle.py` will create these directories and files:

1. `crawled/html/`: the sources of crawled webpages, stripped of `<script>` and `<style>`
2. `crawled/text/`: texts of crawled webpages for indexing
3. `crawled/webpage_list.sqlite`: an SQLite database to store the list of websites crawled
4. `crawled/image_list.sqlite`: an SQLite database to store the list of images crawled

`IndexFiles.py` will create two indices, one in `index/webpages/` for a webpage index and `index/images/` for the image index.
