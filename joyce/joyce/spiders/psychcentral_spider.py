import scrapy
from joyce.items import JoyceItem
import time

class PsychCentral(scrapy.Spider):
	name = "psychcentral"
	allowed_domains = ["psychcentral.com"]
	start_urls = [
		"http://forums.psychcentral.com/health-support/",
	]

	def parse(self, response):
		links_xpath = "//table//a[@style='font-weight:bold']/@href"
		for href in response.xpath(links_xpath):
			url = response.urljoin(href.extract())
			print url
			yield scrapy.Request(url, callback=self.get_all_data)
		next_page_xpath = "//a[text()='>']/@href"
		next_page = response.xpath(next_page_xpath)
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url,callback=self.parse)

	def get_all_data(self,response):

		post_text = response.css('.alt1').xpath('div[2]/text()').extract()
		try:
			post_text = str(post_text[1])
			post_text = post_text.replace('\r','')
			post_text = post_text.replace('\n','')
			post_text = post_text.replace('\t','')
		except:pass

		date = response.css('.thead').xpath('text()').extract()[2]
		date = str(date)
		date = date.replace('\r','')
		date = date.replace('\n','')
		date = date.replace('\t','')


		item = JoyceItem()
		item['author'] = response.css('.bigusername').xpath('text()').extract_first()
		item['author_link'] = response.css('.bigusername').xpath('@href').extract_first()
		item['publish_date'] = date
		item['url'] = response.url
		item['post_text'] = post_text
		yield item


