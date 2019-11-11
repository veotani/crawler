import os
import json
import unittest
from scrapy.crawler import CrawlerProcess

from page_with_cycle_spider import PageWithCycleSpider
from single_page_spider import SinglePageSpider
from single_subpage_spider import SingleSubpageSpider


class TestCrawling(unittest.TestCase):
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
        process.crawl(SingleSubpageSpider)
        process.crawl(PageWithCycleSpider)
        process.start()

    def test_single_page(self):
        single_page_info = None
        with open('results.json') as f:
            for line in f:
                page = json.loads(line)
                for key in page:
                    if "single-page/index.html" in key:
                        single_page_info = page[key]
        if not single_page_info:
            self.fail("single page info not found")
        self.assertEqual(single_page_info['links'], 0)

    def test_one_subpage(self):
        single_page_info = None
        with open('results.json') as f:
            for line in f:
                page = json.loads(line)
                for key in page:
                    if "one-subpage/index.html" in key:
                        single_page_info = page[key]
        if not single_page_info:
            self.fail("single page info not found")
        self.assertEqual(single_page_info['links'], 1)

    def test_pages_with_cycle(self):
        single_page_info = None
        with open('results.json') as f:
            for line in f:
                page = json.loads(line)
                for key in page:
                    if "pages-with-cycle/index.html" in key:
                        single_page_info = page[key]
        if not single_page_info:
            self.fail("single page info not found")
        self.assertEqual(single_page_info['links'], 1)


if __name__ == '__main__':
    unittest.main()

