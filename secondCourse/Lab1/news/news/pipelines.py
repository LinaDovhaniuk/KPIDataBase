# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import pprint

import xml.etree.ElementTree as elementTree
from lxml import etree

DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
NEWS_PATH = 'news.xml'

class NewsPipeline(object):
    def __init__(self):
        self.FILE = ''.join([DIRECTORY_PATH, '/', NEWS_PATH])
        self.graph_count = {}

    def open_spider(self, spider):
        tree = elementTree.ElementTree(elementTree.ElementTree('data'))
        if os.path.exists(self.FILE):
            os.remove(self.FILE)
        tree.write(self.FILE, encoding="utf-8", xml_declaration=True)

    def process_item(self, item, spider):
        tree = elementTree.parse(self.FILE)
        root = tree.getroot()
        page = elementTree.SubElement(root, 'page', url = item['page_url'])

        for page in item['page_texts']:
            elementTree.SubElement(page,'fragment', type = 'text').text = page
        for image in item['page_images']:
            elementTree.SubElement(page,'fragment', type = 'image').text = image
        tree = elementTree.ElementTree(root)
        tree.write(self.FILE,encoding="utf-8", xml_declaration= True)
        # tree.write('news.xml')
        return item

    def close_spider(self, spider):
        data = etree.parse(self.FILE)
        # for element in data.xpath('//image'):
        #     self.graph_count[element.xpath('./@url')[0]] = element.xpath('min(./fragment[@type="image"])')
        #     pprint.pprint(self.graph_count)
