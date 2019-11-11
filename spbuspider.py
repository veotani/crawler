import uspider


class SPBUSpider(uspider.USpider):
    name = "spbuspider"
    allowed_domains = ["spbu.ru"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls.insert(0, "https://spbu.ru")
