# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst

class YelpItem(scrapy.Item):
	Business_Name=scrapy.Field(output_processor = TakeFirst())
	Phone=scrapy.Field(output_processor = TakeFirst())
	Website=scrapy.Field(output_processor = TakeFirst())
	Open_Status=scrapy.Field(output_processor = TakeFirst())
	Rating=scrapy.Field(output_processor = TakeFirst())
	Postal_Code=scrapy.Field(output_processor = TakeFirst())
	Open_Hours=scrapy.Field(output_processor = TakeFirst())
   
