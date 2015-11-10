import scrapy
from joyce.items import JoyceItem
import time

class CancerCompass(scrapy.Spider):
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

		author_name_xpath = "//div[@id='posts']/div[1]/div/div//table/tbody/tr[2]/td//a[@class='bigusername']/text()"
		author_link_xpath = "//div[@id='posts']/div[1]/div/div//table/tbody/tr[2]/td//a[@class='bigusername']/@href"
		author_posted_date_xpath = "//div[@id='posts']/div[1]/div/div//table/tbody/tr[1]/td[1]/text()"
		author_text_xpath = "//div[@id='posts']/div[1]/div/div//table/tbody/tr[2]/td[2]/div[2]/text()"

		item = JoyceItem()
		item['author'] = response.xpath(author_name_xpath).extract()
		item['author_link'] = response.xpath(author_link_xpath).extract()
		item['publish_date'] = response.xpath(author_posted_date_xpath).extract()
		item['url'] = response.url
		item['post_text'] = response.xpath(author_text_xpath).extract()
		yield item


