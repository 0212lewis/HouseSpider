import scrapy
from spider.items import anjukeHouseItem
# 安居客的爬虫脚本
class HouseSpider(scrapy.Spider):

    name = "anjuke"
    start_urls = ["https://sh.fang.anjuke.com/loupan/?from=navigation"]

    #解析函数
    def parse(self, response):
        houselist = response.xpath('//div[@class="key-list imglazyload"]/div')
        for item in houselist:
            index_url = item.xpath('.//div[@class="infos"]/a[@class="lp-name"]/@href').extract_first()
            yield scrapy.Request(index_url, callback=self.index_parse)
        next_url = response.xpath('//div[@class="list-page"]/div[@class="pagination"]/a[@class="next-page next-link"]/@href').extract_first()
        if next_url is not None:
            yield scrapy.Request(next_url, callback=self.parse)

    def index_parse(self, response):
        detail_url = response.xpath('//ul[@class="lp-navtabs clearfix"]/li[2]/a/@href').extract_first()
        yield scrapy.Request(detail_url, callback=self.detail_parse)

    def detail_parse(self, response):
        houseitem = anjukeHouseItem()
        houseitem['city'] = '上海'

        tab1List = response.xpath('//div[@class="can-item"][1]/div[@class="can-border"]/ul/li/div[@class="name"]/text()').extract()
        houseitem['name'] = response.xpath('//div[@class="can-item"][1]/div[@class="can-border"]/ul/li[1]/div[@class="des"]/a/text()').extract_first().strip()

        if ('参考单价' in tab1List) :
            index = str(tab1List.index('参考单价')+1)
            temp = response.xpath('//div[@class="can-item"][1]/div[@class="can-border"]/ul/li[' + index + ']/div[@class="des"]/span/text()').extract_first()
            if temp is not None:
                houseitem['price'] = temp.strip()+"元/㎡"
            else:
                houseitem['price'] = '价格未定'
        else:
            houseitem['price'] = ""
        if ('区域位置' in tab1List) :
            index = str(tab1List.index('区域位置')+1)
            houseitem['field'] = response.xpath('//div[@class="can-item"][1]/div[@class="can-border"]/ul/li[' + index + ']/div[@class="des"]/a[1]/text()').extract_first()
        else:
            houseitem['field'] = ""

        if ('楼盘地址' in tab1List) :
            index = str(tab1List.index('楼盘地址')+1)
            houseitem['address'] = response.xpath('//div[@class="can-item"][1]/div[@class="can-border"]/ul/li[' + index + ']/div[@class="des"]/text()').extract_first().strip()
        else:
            houseitem['address'] = ""

        tab2List = response.xpath('//div[@class="can-item"][2]/div[@class="can-border"]/ul/li/div[@class="name"]/text()').extract()
        if ('楼盘户型' in tab2List) :
            index = str(tab2List.index('楼盘户型')+1)
            houseitem['huxing'] = response.xpath('//div[@class="can-item"][2]/div[@class="can-border"]/ul/li[' + index + ']/div[@class="des"]/text()').extract_first().strip()
            houseitem['huxing'] = houseitem['huxing'].replace('\n', "").replace('\r', "").replace(" ", "")
        else:
            houseitem['huxing'] = ""
        if ('交房时间' in tab2List) :
            index = str(tab2List.index('交房时间')+1)
            houseitem['submitTime'] = response.xpath('//div[@class="can-item"][2]/div[@class="can-border"]/ul/li[' + index + ']/div[@class="des"]/text()').extract_first().strip()
        else:
            houseitem['submitTime'] = ""

        tab3List = response.xpath('//div[@class="can-item"][3]/div[@class="can-border"]/ul/li/div[@class="name"]/text()').extract()
        if ('规划户数' in tab3List) :
            index = str(tab3List.index('规划户数')+1)
            houseitem['hushu'] = response.xpath('//div[@class="can-item"][3]/div[@class="can-border"]/ul/li[' + index + ']/div[@class="des"]/text()').extract_first().strip()
        else:
            houseitem['hushu'] = ""
        if ('建筑类型' in tab3List) :
            index = str(tab3List.index('建筑类型')+1)
            houseitem['type'] = response.xpath('//div[@class="can-item"][3]/div[@class="can-border"]/ul/li[' + index + ']/div[@class="des"]/text()').extract_first().strip()
        else:
            houseitem['type'] = ""

        if ('楼层状况' in tab3List):
            index = str(tab3List.index('楼层状况')+1)
            houseitem['louceng'] = response.xpath('//div[@class="can-item"][3]/div[@class="can-border"]/ul/li[' + index + ']/div[@class="des"]/text()').extract_first().strip()
        else:
            houseitem['louceng'] = ""
        print(houseitem)
        # yield houseitem
