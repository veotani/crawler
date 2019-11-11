import uspider


class MSUSpider(uspider.USpider):
    name = "msuspider"
    allowed_domains = ["msu.ru"]
    download_delay = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls.insert(0, "https://msu.ru")
