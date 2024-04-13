import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class EventSpider(scrapy.Spider):
    name = 'event_spider'
    start_urls = ['https://example.com/events', 'https://another-example.com/events']

    def parse(self, response):
        events = response.css('div.event')
        for event in events:
            yield {
                'title': event.css('h2.title::text').get(),
                'date': event.css('span.date::text').get(),
                'location': event.css('span.location::text').get(),
                'description': event.css('p.description::text').get(),
                'url': event.css('a.url::attr(href)').get()
            }

def run_spider(spider_name):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_name)
    process.start()

