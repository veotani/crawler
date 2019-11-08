import uspider


class SPBUSpider(uspider.USpider):
    name = "spbuspider"
    start_urls = ["https://spbu.ru"]
    allowed_domains = ["spbu.ru"]
