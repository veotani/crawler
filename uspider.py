import scrapy
from urllib.parse import urljoin

class USpider(scrapy.Spider):
    links = set()
    visited = {}
    custom_settings = {'HTTPERROR_ALLOW_ALL': True}
    download_delay = 0.25
        
    def parse_link(self, link, start_url):
        link = urljoin(start_url, link)
        if link.startswith("http://"):
            new_link = link[7:]
        elif link.startswith("https://"):
            new_link = link[8:]
        else:
            return {
                "type": "other"
            }
        if new_link.startswith("www."):
            new_link = new_link[4:]
        domain_index = new_link.find(self.allowed_domains[0])
        if domain_index == -1:
            return {
                "type": "external"
            }
        if domain_index == 0:
            return {
                "type": "internal",
                "link": link
            }
        return {
            "type": "subdomain",
            "subdomain": new_link[:domain_index-1]
        }
        
    def parse(self, response):
        result = {
            "type": "internal",
            "status": response.status
        }
        if response.status == 200:
            result["length"] = len(response.body)
            try:
                links = response.xpath("//a/@href").extract()
            except:
                links = []
            result["links"] = len(links)
        else:
            links = []
        self.visited[response.url] = result
        yield {response.url: self.visited[response.url]}
        for link in links:
            if link in self.links:
                continue
            self.links.add(link)
            parsed_url = self.parse_link(link, response.url)
            if parsed_url["type"] == "internal":
                yield response.follow(parsed_url["link"], self.parse)
            else:
                yield {link: parsed_url}