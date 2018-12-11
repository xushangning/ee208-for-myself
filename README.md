# 001-(2018-2019-1)EE208

## Directory Structure

Running `parallel_crawle.py` will create these directories and files:

1. `crawled/html/`: the sources of crawled webpages, stripped of `<script>` and `<style>`
2. `crawled/text/`: texts of crawled webpages for indexing
3. `crawled/webpage_list.sqlite`: an SQLite database to store the list of websites crawled
4. `crawled/image_list.sqlite`: an SQLite database to store the list of images crawled

`IndexFiles.py` will create two indices, one in `index/webpages/` for a webpage index and `index/images/` for the image index.

## Database

There are two databases for the list of images and webpages. The scheme for the table of webpages is

Column | Description
--- | ---
`url` | the URL of the webpage
`title` | the title of the webpage
`filename` | the name of the file where the source and texts of the webpage are stored

The scheme for the table of images is

Column | Description
--- | ---
`url` | the URL of the image
`description` | the description of the image
`origin` | the URL of the webpage into which the image is embeded

## References

- [Apache Lucene 7.5.0 Documentation](https://lucene.apache.org/core/7_5_0/)
- [Hadoop – Apache Hadoop 3.1.1](https://hadoop.apache.org/docs/r3.1.1/)

### Image Processing

- [OpenCV: OpenCV modules](https://docs.opencv.org/4.0.0/)
- [SIFT: Theory and Practice: Introduction - AI Shack](http://aishack.in/tutorials/sift-scale-invariant-feature-transform-introduction/)
