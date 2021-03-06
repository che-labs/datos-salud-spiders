# class MusicSpider(scrapy.Spider):
# 	name = "music"
# 	allowed_domains = ["musicforprogramming.net"]
# 	start_urls = ['http://musicforprogramming.net/']
#
# 	count = 0
#
# 	def parse(self, response):
# 		# The name alone contains u'musicForProgramming("47: Abe Mangger");'
# 		# So we strip out to get the name of the song only
# 		title = response.css('title::text').extract_first()[len('musicForProgramming("'):-3]
# 		src = response.xpath('//audio[@id="player"]/@src').extract_first()
#
# 		self.count += 1
# 		if self.count >= 46:
# 			return
#
# 		yield Songs(title=title, file_urls=[src])
#
# 		next_url = response.xpath('//div[@id="episodes"]/a/@href').extract()[self.count]
#
# 		if next_url is not None:
# 			yield scrapy.Request(response.urljoin('http://musicforprogramming.net/' + next_url))