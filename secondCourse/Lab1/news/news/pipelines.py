# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import pprint
import logging
import xml.etree.ElementTree as elementTree
from lxml import etree

DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
NEWS_PATH = 'news.xml'
PRODUCTS_XML_FILE = 'products.xml'
PRODUCTS_XSL_FILE = 'products.xsl'

logger = logging.getLogger("logger")
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
        with open('L:/KPI/DataBase/Second_Course/Lab1/news/news/tmptxt.txt', 'a') as f:
            f.write('\n\nALAAAAAAARM\n{}\n\n'.format(str(item)))

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

        for element in data.xpath('//image'):
            self.graph_count[element.xpath('./@url')[0]] = element.xpath('min(count(./fragment[@type="image"]))')
            pprint.pprint(self.graph_count)


# class ProductPipeline(object):
#
#     def __init__(self):
#         self.XML_FILE = ''.join([DIRECTORY_PATH, '/', PRODUCTS_XML_FILE])
#         self.XSL_FILE = ''.join([DIRECTORY_PATH, '/', PRODUCTS_XSL_FILE])
#
#     def open_spider(self, spider):
#         tree = elementTree.ElementTree(elementTree.Element('items'))
#         if os.path.exists(self.XML_FILE):
#             os.remove(self.XML_FILE)
#         tree.write(self.XML_FILE, encoding="utf-8", xml_declaration=True)
#
#     def process_item(self, item, spider):
#         tree = elementTree.parse(self.XML_FILE)
#         root = tree.getroot()
#         page = elementTree.SubElement(root, 'item')
#         elementTree.SubElement(page, 'title').text = item['title']
#         elementTree.SubElement(page, 'description').text = item['description']
#         elementTree.SubElement(page, 'price').text = item['price']
#         elementTree.SubElement(page, 'image').text = item['image']
#         tree = elementTree.ElementTree(root)
#         tree.write(self.XML_FILE, encoding="utf-8", xml_declaration=True)
#         return item
#
#     def close_spider(self, spider):
#         dom = etree.parse(self.XML_FILE)
#         xslt = etree.parse(self.XSL_FILE)
#         transform = etree.XSLT(xslt)
#         newdom = transform(dom)
#         with open(DIRECTORY_PATH + '/products.html', 'wb') as f:
#             f.write(etree.tostring(newdom, pretty_print=True))
#         with open(DIRECTORY_PATH + '/products.xhtml', 'wb') as f:
#             f.write(etree.tostring(newdom, pretty_print=True))
#
