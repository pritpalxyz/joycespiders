import scrapy
from joyce.items import JoyceItem
import time
from bs4 import BeautifulSoup
import re
class InspireSpider(scrapy.Spider):
	name = "inspires"
	allowed_domains = ["inspire.com"]
	start_urls = [
		"https://www.inspire.com/groups/leukemia-lymphoma-and-myeloma/new/active/?page=1",
	]


	def parse(self, response):
		links_path = "//div[@id='search-results']//h3//a/@href"
		for href in response.xpath(links_path):
			url = response.urljoin(href.extract())
			print url
			yield scrapy.Request(url, callback=self.get_main_data)
		next_page_xpath = "//a[text()='Next >']/@href"
		next_page = response.xpath(next_page_xpath)
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url,callback=self.parse)

	
			
	def parseText(self, str):
		soup = BeautifulSoup(str, 'html.parser')
		return re.sub(" +|\n|\r|\t|\0|\x0b|\xa0",' ',soup.get_text()).strip()

	def cleanText(self,text):
		soup = BeautifulSoup(text,'html.parser')
		text = soup.get_text();
		text = re.sub("( +|\n|\r|\t|\0|\x0b|\xa0|\xbb|\xab)+",' ',text).strip()
		return text 

	def get_main_data(self,response):
		author_name_xpath = "//li[@class='by']/a/text()"
		author_link = "//li[@class='by']/a/@href"
		author_posted_date_xpath = "//li[@class='by']/text()"
		post_body_xpath = "//div[@class='post-body']/p/text()"
		date = response.xpath(author_posted_date_xpath).extract()[1]
		date = self.cleanText(self.parseText(date))
		date = date.split('')
		item = JoyceItem()
		item['author'] = response.xpath(author_name_xpath).extract_first()
		item['author_link'] = response.xpath(author_link).extract()
		item['publish_date'] = date
		item['url'] = response.url
		item['post_text'] = response.xpath(post_body_xpath).extract()
		yield item


