import scrapy
from joyce.items import JoyceItem
import time

class CancerCompass(scrapy.Spider):
	name = "lymphomas"
	allowed_domains = ["lymphomas.org.uk"]
	start_urls = [
		"http://www.lymphomas.org.uk/forum",
	]


	def parse(self,response):
		links_xpath = "//div[@class='forum-name']/a/@href"
		for href in response.xpath(links_xpath):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.get_all_data)

	def get_all_data(self,response):
		links_xpath_sub = "//span[@class='forum-topic-title']/../@href"
		for href in response.xpath(links_xpath_sub):
			url = response.urljoin(href.extract())
			print url
			yield scrapy.Request(url, callback=self.get_main_data)

		next_page_xpath = "//li[@class='pager-next']/a/@href"
		next_page = response.xpath(next_page_xpath)
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url,callback=self.parse)

	def get_main_data(self,response):
		author_name_xpath = "//div[@id='content']/div[3]//span[@class='username']/text()"
		author_link_xpath = "//div[@id='content']/div[3]//span[@class='username']/@about"
		author_date_posted_xpath = "//div[@id='content']/div[3]/div[1]/div[1]/span/text()"
		author_text_xpath = "//div[@id='content']/div[3]//div[@class='field-items']//p/text()"

		author_link = "https://www.lymphomas.org.uk%s"%response.xpath(author_link_xpath).extract()[0]

		item = JoyceItem()
		item['author'] = response.xpath(author_name_xpath).extract()
		item['author_link'] = author_link
		item['publish_date'] = response.xpath(author_date_posted_xpath).extract()
		item['url'] = response.url
		item['post_text'] = response.xpath(author_text_xpath).extract()
		yield item