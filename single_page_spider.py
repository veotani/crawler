import uspider

class SinglePageSpider(uspider.USpider):
    name = "single_page_spider"
    start_urls = ["file:///home/veotani/dev/crawler/mock/single-page/index.html"]
