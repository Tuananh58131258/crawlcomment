from scrapy import Spider
from scrapy.selector import Selector
import scrapy
from crawler.items import CrawlerItem


class DataCrawler(Spider):
    name = "spider"
    allowed_domains = ["fptshop.com.vn"]
    start_urls = ["https://fptshop.com.vn/dien-thoai/apple-iphone",
                  "https://fptshop.com.vn/dien-thoai/samsung", 
                  "https://fptshop.com.vn/dien-thoai/oppo",
                  "https://fptshop.com.vn/dien-thoai/xiaomi",
                  "https://fptshop.com.vn/dien-thoai/vivo",
                  "https://fptshop.com.vn/dien-thoai/huawei",
                  ]

    def parse(self, response):
        san_pham = response.xpath(
            '/html/body/section/div/div[2]/div[2]/div[3]/div')
        base_url = "https://fptshop.com.vn/"
        for item in san_pham[1:]:
            ten_dien_thoai = item.xpath('a/@href').get()
            link = base_url + ten_dien_thoai
            yield scrapy.Request(link, callback=self.crawldata)

    def crawldata(self, response):
        questions = response.xpath(
            '//*[@id="list-comment"]/div[@class="f-cmt-ask"]')
        for quest in questions[1:]:
            items = CrawlerItem()
            items['Comment'] = quest.xpath(
                'div[@class="f-cmmain"]/text()').extract_first()
            yield items
