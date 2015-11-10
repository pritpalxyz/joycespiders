import scrapy
from joyce.items import JoyceItem
import time
from selenium import webdriver

class DailyStrength(scrapy.Spider):
	name = "dailystrength"
	allowed_domains = ["dailystrength.org"]
	start_urls = [
		"http://www.dailystrength.org/c/Chronic-Lymphocytic-Leukemia-CLL/forum",
	]

	def parse(self, response):
		driver = webdriver.Firefox()
		driver.get(response.url)
		links_xpath = "//table[@class='discussion_listing_main'][2]//tr/td[2]/a"
		links_lists = []
		for pageno in range(1,100):
			makeurl ="http://www.dailystrength.org/c/Chronic-Lymphocytic-Leukemia-CLL/forum/page-%s"%pageno
			driver.get(makeurl)
			time.sleep(3)
			get_links = driver.find_elements_by_xpath(links_xpath)
			total_links = len(get_links)
			if total_links == 0:
				break
			for i in get_links:
				links_lists.append(i.get_attribute('href'))
		driver.close()
		for url in links_lists:
			yield scrapy.Request(url,callback=self.get_sub_data)


	def get_sub_data(self,response):
		author_name_xpath = "//table[@class='discussion_topic']//p[@class='username']/a/text()"
		author_link_xpath = "//table[@class='discussion_topic']//p[@class='username']/a/@href"
		author_posted_xpath = "//table[@class='discussion_topic']//div/span[@class='graytext']/text()"
		author_all_text_xpath = "//table[@class='discussion_topic']//div[@class='discussion_text longtextfix485']/text()"

		author_name = response.xpath(author_name_xpath).extract()
		author_name = str(author_name[0])
		author_name = author_name.replace("\t","")



		author_name = author_name.replace(',',' ')
		author_link = response.xpath(author_link_xpath).extract()
		author_link  = author_link[0]
		author_link = "http://www.dailystrength.org%s"%author_link
		author_posted = response.xpath(author_posted_xpath).extract()
		author_posted = author_posted[0]
		author_posted = author_posted.replace(',','')
		author_posted = author_posted.replace('Posted on','')

		author_all_text = response.xpath(author_all_text_xpath).extract()
		author_all_text = str(author_all_text[0])
		author_all_text = author_all_text.replace(',','')
		author_all_text = author_all_text.replace('\t','')
		author_all_text = author_all_text.replace('  ','')
		author_all_text = author_all_text.replace('\n','')

		item = JoyceItem()

		item['author'] = author_name
		item['author_link'] = author_link
		item['publish_date'] = author_posted
		item['url'] = response.url
		item['post_text'] = author_all_text
		yield item

