import scrapy

class USpider(scrapy.Spider):
    links = set()
    visited = {}
        
    def parse_link(self, link, start_url):
        if link[0] == "/":
            return {
                "type": "internal", 
                "link": start_url + link
            }
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
        try:
            urls = response.xpath("//a/@href").extract()
        except:
            urls = []
        self.visited[response.url] = {
            "type": "internal",
            "status": response.status,
            "length": len(response.body),
            "links": len(urls)
        }
        yield {response.url: self.visited[response.url]}
        for url in urls:
            if url in self.links:
                continue
            self.links.add(url)
            parsed_url = self.parse_link(url, response.url)
            domain_index = url.find(self.allowed_domains[0])
            if parsed_url["type"] == "internal":
                yield response.follow(parsed_url["link"], self.parse)
            else:
                yield {url: parsed_url}