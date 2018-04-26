import scrapy
from news.items import NewsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class News_Spider(scrapy.Spider):
   name = "newsSpider"

   # custom_settings = {
   #     'ITEM_PIPELINES': {
   #         'news.pipelines.NewsPipeline': 800
   #     }
   # }

   start_urls = {
      'https://tsn.ua/'
   }


   def parse(self, response):
      for tmp in response.xpath('//div[@class="c-entry-embed"]/a/@href'):
         yield response.follow(tmp, callback = self.parse_item)


   def parse_item(self, response):
      def extract_all_xpath(query):
         return response.xpath(query).extract()

      texts = []
      for text in extract_all_xpath('//p/text()'):
         text = text.rstrip()
         if len(text) is not 0:
            texts.append(text)
      yield NewsItem(page_url = response.request.url,
                     page_texts = texts,
                     page_images = extract_all_xpath('//img/@src'))