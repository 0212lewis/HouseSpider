# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from openpyxl import Workbook


class ExcelPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['城市名', '小区名', '地址', '小区类型', '栋数', '小区户数', '平均价格'])

    def process_item(self, item, spider):
        line = [item['city'], item['name'], item['address'], item['type'], item['ridgepole'],
                item['hushu'], item['price']]
        self.ws.append(line)
        self.wb.save('lianjia.xlsx')
        return item
