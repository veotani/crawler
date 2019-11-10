import uspider

class PageWithCycleSpider(uspider.USpider):
    name = "page_with_cycle_spider"
    start_urls = ["file:///home/veotani/dev/crawler/mock/pages-with-cycle/index.html"]
