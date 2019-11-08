import uspider


class MSUSpider(uspider.USpider):
    name = "msuspider"
    start_urls = ["https://msu.ru"]
    allowed_domains = ["msu.ru"]
    download_delay = 1
