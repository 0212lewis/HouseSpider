import scrapy
from spider.items import lianjiaHouseItem

class HouseSpider(scrapy.Spider):

    name = "lianjia"
    start_urls = ['https://sh.lianjia.com/xiaoqu/?from=rec']

    page_num = 1

    def parse(self, response):
        houseList = response.xpath('//ul[@class="listContent"]/li[@class="clear xiaoquListItem"]')
        for item in houseList:
            houseItem = lianjiaHouseItem()
            houseItem['city'] = '上海'
            addressList = item.xpath('.//div[@class="info"]/div[@class="positionInfo"]/a/text()').extract()
            houseItem['address'] = addressList[0]+" "+addressList[1]
            detail_url = item.xpath('.//div[@class="info"]/div[@class="title"]/a/@href').extract_first()
            yield scrapy.Request(detail_url, callback=self.detail_parse, meta={"houseItem": houseItem})
        next_page = 'https://sh.lianjia.com/xiaoqu/pg'+str(self.page_num) + '/?from=rec'
        self.page_num = self.page_num + 1
        if self.page_num < 31:
            yield scrapy.Request(next_page, callback=self.parse)

    def detail_parse(self, response):
        houseItem = response.meta["houseItem"]
        houseItem['name'] = response.xpath('//div[@class="detailHeader fl"]/h1[@class="detailTitle"]/text()').extract_first().strip()

        priceTemp = response.xpath('//div[@class="xiaoquPrice clear"]/div[@class="fl"]/span[1]/text()').extract_first()
        if priceTemp is not None:
            houseItem['price'] = priceTemp.strip()+"元/㎡"
        else:
            houseItem['price'] = "暂无挂牌均价"
        tabList = response.xpath('//div[@class="xiaoquInfo"]/div[@class="xiaoquInfoItem"]/span[@class="xiaoquInfoLabel"]/text()').extract()
        if ('建筑类型' in tabList) :
            index = str(tabList.index('建筑类型')+1)
            houseItem['type'] = response.xpath('//div[@class="xiaoquInfo"]/div[@class="xiaoquInfoItem"][' + index + ']/span[@class="xiaoquInfoContent"]/text()').extract_first().strip()
        else:
            houseItem['type'] = ''
        if ('楼栋总数' in tabList) :
            index = str(tabList.index('楼栋总数')+1)
            houseItem['ridgepole'] = response.xpath('//div[@class="xiaoquInfo"]/div[@class="xiaoquInfoItem"][' + index + ']/span[@class="xiaoquInfoContent"]/text()').extract_first().strip()
        else:
            houseItem['ridgepole'] = ''
        if ('房屋总数' in tabList) :
            index = str(tabList.index('房屋总数')+1)
            houseItem['hushu'] = response.xpath('//div[@class="xiaoquInfo"]/div[@class="xiaoquInfoItem"][' + index + ']/span[@class="xiaoquInfoContent"]/text()').extract_first().strip()
        else:
            houseItem['hushu'] = ''
        # print(houseItem)
        yield houseItem

