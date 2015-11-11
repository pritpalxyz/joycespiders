import scrapy
from joyce.items import JoyceItem

class CancerFourms(scrapy.Spider):
	name = "cancerforums"
	allowed_domains = ["*"]
	start_urls = [
		"http://www.cancerforums.net/threads/205-CLL",
	]

	def parse(self, response):
		links_path = "//li[@class='postbitlegacy postbitim postcontainer old']"
		
		for data in response.xpath(links_path):	
			item = JoyceItem()
			item['author'] = response.xpath("//div[@class='userinfo']//span/text()").extract()
			item['author_link'] = ''
			item['publish_date'] = response.xpath("//span[@class='date']/text()").extract()
			item['url'] = response.url
			item['post_text'] = response.xpath("//div[@class='content']/div/blockquote/text()").extract()
			yield item

		next_page_xpath = "//a[@rel='next']/@href"
		next_page = response.xpath(next_page_xpath)
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url,callback=self.parse)			

