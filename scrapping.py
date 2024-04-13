import scrapy
import json
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from flask import Flask, jsonify


class EventSpider(scrapy.Spider):
    name = 'event_spider'
    start_urls = ['https://biberlin.de/', 'https://www.schwuz.de/', 'https://sonntags-club.de/']

    def parse(self, response):
        # print(response.status)
        # print(response.headers)
        # print(response.text)
        if response.url == 'https://biberlin.de/':
            events = response.css('div.event')
            for event in events:
                yield {
                    'title': event.css('h2.title::text').get(),
                    'date': event.css('span.date::text').get(),
                    'location': event.css('span.location::text').get(),
                    'description': event.css('p.description::text').get(),
                    'url': event.css('a.url::attr(href)').get()
                }      
        if response.url == 'https://www.schwuz.de/':
            events = response.css('div.sc_events_item')
            for event in events:
                yield {
                    # 'location': event.css('p.location::text').get(),
                    'title': event.css('h3.sc_events_item_title::text').get(),
                    'date': event.css('span.sc_events_item_date::text').get(),
                    'description': event.css('sc_events_item_text p::text').get(),
                    'url': response.urljoin(event.css('a.sc_events_item_link::attr(href)').get()),
                    'fee': event.css('span.sc_events_item_price::text').get(),
                }
        elif response.url == 'https://sonntags-club.de/':
            events = response.css('div.event')
            for event in events:
                yield {
                    'title': event.css('div.eventlist-event-info h2::text').get(),
                    'date': event.css('div.eventlist-event-info div.date::text').get(),
                    'location': 'Sonntags Club',
                    'description': event.css('div.eventlist-event-info div.excerpt p::text').get(),
                    'url': response.urljoin(event.css('div.eventlist-event-info a::attr(href)').get())
                }

def run_spider(spider_name):
    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'json')
    settings.set('FEED_URI', 'result.json')
    
    process = CrawlerProcess(get_project_settings())
    process.crawl(EventSpider)
    process.start()


app = Flask(__name__)

# @app.route('/')
# def index():
#     return jsonify({'message': 'Welcome to the Event Scraper API!'})

# @app.route('/api/events', methods=['GET'])
# # def get_events():
# #     try:
# #         with open('result.json', 'r') as f:
# #             data = json.load(f)
# #         return jsonify(data)
# #     except FileNotFoundError:
# #         return jsonify({'message': 'No events data available. Please run the scraper first.'}), 404
# def get_events():
#     print("Current working directory:", os.getcwd())
#     print("Files in current working directory:", os.listdir(os.getcwd()))
#     try:
#         with open('result.json', 'r') as f:
#             data = json.load(f)
#         return jsonify(data)
#     except FileNotFoundError:
#         return jsonify({'message': 'No events data available. Please run the scraper first.'}), 404

# if __name__ == "__main__":
#     run_spider('event_spider')
#     app.run(debug=True, port=9000)
    



app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Event Scraper API!'})

@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        with open('result.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'message': 'No events data available. Please run the scraper first.'}), 404

if __name__ == "__main__":
    run_spider('event_spider')
    app.run(debug=True, port=9001)
    











# @app.route('/api/events', methods=['GET'])
# def get_events():
#     with open('result.json', 'r') as f:
#         data = json.load(f)
#     return jsonify(data)

# if __name__ == "__main__":
#     run_spider('event_spider')
#     app.run(debug=True, port=8000)

    # process.stop()

# def print_results():
#     with open('result.json', 'r') as f:
#         data = json.load(f)
#         for item in data:
#             print(item)
            
# if __name__ == "__main__":
#     run_spider('event_spider')
#     print_results()