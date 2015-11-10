# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JoyceItem(scrapy.Item):

	author = scrapy.Field()
	author_link = scrapy.Field()
	publish_date = scrapy.Field()
	url = scrapy.Field()
	post_text  = scrapy.Field()
	pass
