import scrapy
from joyce.items import JoyceItem

class CancerCompass(scrapy.Spider):
	name = "cancercompass"
	allowed_domains = ["cancercompass.com"]
	start_urls = [
		"http://www.cancercompass.com/message-board/cancers/leukemia/leukemia-(cll)/1,0,119,7,50.htm",
	]

	def parse(self, response):
		for href in response.xpath("//a[@class='subLink']/@href"):
			url = response.urljoin(href.extract())
			print url
			yield scrapy.Request(url, callback=self.get_all_data)
		next_page = response.xpath("//a[text()='Next']/@href")
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url,callback=self.parse)

	def get_all_data(self, response):
		author_name_xpath  = "//div[@class='mbpost'][1]//div[@class='author']/p/a/span/text()"
		author_link_xpath  = "//div[@class='mbpost'][1]//div[@class='author']/p/a/@href"
		publish_date_xpath = "//div[@class='mbpost'][1]//div[@class='message']/div[@class='header']/p/text()" #remove "By" and "on"
		post_text_xpath    = "//div[@class='mbpost'][1]//div[@class='message']/div[@class='msgContent']/p/text()" 

		author_name = response.xpath(author_name_xpath).extract()

		author_link = response.xpath(author_link_xpath).extract()
		author_link  = "http://www.cancercompass.com%s"%(author_link[0])

		publish_date = response.xpath(publish_date_xpath).extract()
		publish_date =  str(publish_date[1])
		publish_date = publish_date.replace('on','')


		post_text = response.xpath(post_text_xpath).extract()
		if post_text == '':
			post_text = response.xpath("//div[@class='mbpost'][1]//div[@class='msgContent']/text()").extract()

		item = JoyceItem()

		item['author'] = response.xpath(author_name_xpath).extract()
		item['author_link'] = author_link
		item['publish_date'] = publish_date
		item['url'] = response.url
		item['post_text'] = post_text
		yield item