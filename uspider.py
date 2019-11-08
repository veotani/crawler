import scrapy
import sqlite3
import os
from urllib.parse import urljoin


class USpider(scrapy.Spider):
    name = "unnamed_spider"
    links = set()
    visited = {}
    custom_settings = {'HTTPERROR_ALLOW_ALL': True}
    download_delay = 0.25

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not os.path.exists(f"{self.name}.db"):
            os.mknod(f"{self.name}.db")
        self.conn = sqlite3.connect(f"{self.name}.db")
        self.conn.cursor().execute("""
        CREATE TABLE IF NOT EXISTS links (
        url TEXT PRIMARY KEY,
        type TEXT NOT NULL,
        status INTEGER,
        length INTEGER,
        links INTEGER,
        subdomain TEXT,
        visited INTEGER,
        completed INTEGER )
        """)
        self.conn.commit()

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
        cursor = self.conn.cursor()
        cursor.execute(f"""
        INSERT INTO links (url, type, status, length, links, visited, completed) 
        VALUES (
        {response.url},
        'internal',
        {response.status},
        {result.get('length'), 'NULL'},
        {result.get('links'), 'NULL'},
        {result.get('subdomain'), 'NULL'},
        1,
        0)
        """)
        self.conn.commit()
        yield {response.url: result}
        for link in links:
            cursor.execute(f"SELECT COUNT(*) FROM links WHERE url={link}")
            if not cursor.fetchall()[0]:
                continue
            self.links.add(link)
            parsed_url = self.parse_link(link, response.url)
            if parsed_url["type"] == "internal":
                yield response.follow(parsed_url["link"], self.parse)
            else:
                yield {link: parsed_url}
