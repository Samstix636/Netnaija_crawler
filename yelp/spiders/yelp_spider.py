# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scraper_api import ScraperAPIClient
import time 
from yelp.utils import get_urls
import logging
from yelp.items import YelpItem
from scrapy.loader import ItemLoader
# client = ScraperAPIClient('1ea2be17b2cfb9278aae6b9c776a334b')

# API = '1ea2be17b2cfb9278aae6b9c776a334b'
# user_accounts = ['nike', 'adidas'] 
# =============================================================================
# def get_url(url):
#     payload = {'api_key': API, 'url': url}
#     proxy_url = 'https://api.scraperapi.com/?' + urlencode(payload)
#     return proxy_url
# =============================================================================

class YelpSpiderSpider(scrapy.Spider):
    name = 'yelp_spider'
    allowed_domains = ['www.yelp.co.uk']
    # start_urls = get_urls()

    # start_urls = ['https://www.yelp.com/search?find_desc=Plumbers&find_loc=San+Francisco%2C+CA&ns=1']
    # meta = {
    #         "proxy": "http://scraperapi:1ea2be17b2cfb9278aae6b9c776a334b@proxy-server.scraperapi.com:8001"}
    def start_requests(self):
        for url in get_urls():
            yield Request(url, callback=self.parse )

    page=1
    def parse(self, response):
        containers=response.xpath("//a[contains(@href, 'biz') and contains(@class, 'lemon--a__373c0__IEZFH link__373c0__1UGBs link-color--inherit__373c0__1J-tq link-size--inherit__373c0__3K_7i')]/@href").extract()
        print('=========================================')
        print(len(containers))
        for container in containers:
            if 'adredir' not in container:   
                next_url='https://www.yelp.co.uk'+container
                yield scrapy.Request(
                    url=next_url, 
                    callback=self.parse_page, dont_filter=True)
            else:
                pass

        if self.page <=2:
            self.page+=1
            next_page=response.xpath("//a[contains(@class, 'next-link')]/@href").extract_first()
            absolute_url ='https://www.yelp.co.uk' + next_page 
            logging.info("Moving to next page")
            yield Request(url=absolute_url, callback=self.parse, dont_filter=True)
        else:
            pass


    def parse_page(self, response):
        Names=response.css("div.lemon--div__373c0__1mboc.margin-b1__373c0__1khoT.border-color--default__373c0__3-ifU>h1.lemon--h1__373c0__2ZHSL.heading--h1__373c0___56D3.undefined.heading--inline__373c0__1jeAh::text").extract_first()
        Phone=response.xpath("//p[contains(text(), 'Phone number')]/following-sibling::p/text()").extract_first()
        Website= response.xpath("//a[@rel='noopener']/text()").extract_first()
        Open_Status = response.xpath("//span[contains(@class, 'status')]/text()").extract_first()
        Postal_code=response.xpath("//address/p/span/text()").extract()
        rating = response.css("div.lemon--div__373c0__1mboc.i-stars__373c0__1T6rz.i-stars--large-1__373c0__1kclN.border-color--default__373c0__3-ifU.overflow--hidden__373c0__2y4YK::attr(aria-label)").extract_first()
        days= response.xpath("//tbody[@class='lemon--tbody__373c0__2T6Pl']/tr/th/p/text()").getall()
        hrs = response.xpath("//tbody[@class='lemon--tbody__373c0__2T6Pl']//p[contains(@class, 'no-wrap')]/text()").getall()
        mon= days[0] +'--'+ hrs[0]
        tue= days[1] + '--'+ hrs[1]
        wed= days[2] + '--'+hrs[2]
        thu= days[3] +'--'+ hrs[3]
        fri= days[4] + '--'+hrs[4]
        sat= days[5] +'--'+ hrs[5]
        sun= days[6] + '--'+hrs[6]
        total = mon+'\n'+ tue+ '\n'+ wed+ '\n'+ thu+ '\n'+ fri +'\n' +sat +'\n' +sun
        loader= ItemLoader(item=YelpItem())

        loader.add_value("Business_Name", Names)
        loader.add_value("Phone", Phone)
        loader.add_value("Website", Website)
        loader.add_value("Open_Status", Open_Status)
        loader.add_value("Postal_Code", Postal_code)
        loader.add_value("Rating", rating)
        loader.add_value("Open_Hours", total)
        return loader.load_item()

        # yield{
        #     "Business Name":Names,
        #     "Phone":Phone,
        #     "Website":Website,
        #     "Open_Status":Open_Status,
        #     "Rating":rating,
        #     "Postal_code":Postal_code[-1],
        #     'Open_Hours': total

        # }


