import uspider


class CountLinksSpider(uspider.USpider):
    name = "count_links_spider"
    start_urls = ["file:///home/veotani/dev/crawler/mock/count-links/index.html"]
