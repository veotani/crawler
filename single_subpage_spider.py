import uspider

class SingleSubpageSpider(uspider.USpider):
    name = "single_subpage_spider"
    start_urls = ["file:///home/veotani/dev/crawler/mock/one-subpage/index.html"]
