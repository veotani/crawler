import json
import os
import unittest

from scrapy.crawler import CrawlerProcess

from single_page_spider import SinglePageSpider
from stats import get_stats


class TestStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Single page crawler
        if os.path.exists('results.json'):
            os.remove('results.json')
        process = CrawlerProcess(settings={
            'FEED_FORMAT': 'jsonlines',
            'FEED_URI': 'results.json'
        })
        process.crawl(SinglePageSpider)
        process.start()

    def test_get_stats(self):
        data = []
        with open('results.json') as f:
            for line in f:
                data.append(json.loads(line))
        links, subdomains, counters, total_space, total_links, status = get_stats([data])
        self.assertEqual(total_space, 283)
        self.assertEqual(total_links, 0)
        self.assertEqual(status[200], 1)


if __name__ == '__main__':
    unittest.main()
