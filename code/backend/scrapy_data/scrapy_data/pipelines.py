# -*- coding: utf-8 -*-
import json
import re
import logging
from scrapy.utils.project import get_project_settings
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class bublelistPipeline(object):
# 	b420100_district = None
# 	b420100_bizcircle = None
# 	b420100_community = None
# 	b420100_community_id = None
# 	b310000_district = None
# 	b310000_bizcircle = None
# 	b310000_community = None
# 	b310000_community_id = None
# 	b110000_district = None
# 	b110000_bizcircle = None
# 	b110000_community = None
# 	b110000_community_id = None
# 	def open_spider(self, spider):
# 		if spider.name == 'bk_bublelist':
# 			self.b420100_district = open('../data_db/bublelist/420100_district.jsonl', 'w', encoding='utf-8')
# 			self.b420100_bizcircle = open('../data_db/bublelist/420100_bizcircle.jsonl', 'w', encoding='utf-8')
# 			self.b420100_community = open('../data_db/bublelist/420100_community.jsonl', 'w', encoding='utf-8')
# 			self.b420100_community_id = open('../data_db/community_id/420100_community_id.l', 'w', encoding='utf-8')
# 			self.b310000_district = open('../data_db/bublelist/310000_district.jsonl', 'w', encoding='utf-8')
# 			self.b310000_bizcircle = open('../data_db/bublelist/310000_bizcircle.jsonl', 'w', encoding='utf-8')
# 			self.b310000_community = open('../data_db/bublelist/310000_community.jsonl', 'w', encoding='utf-8')
# 			self.b310000_community_id = open('../data_db/community_id/310000_community_id.l', 'w', encoding='utf-8')
# 			self.b110000_district = open('../data_db/bublelist/110000_district.jsonl', 'w', encoding='utf-8')
# 			self.b110000_bizcircle = open('../data_db/bublelist/110000_bizcircle.jsonl', 'w', encoding='utf-8')
# 			self.b110000_community = open('../data_db/bublelist/110000_community.jsonl', 'w', encoding='utf-8')
# 			self.b110000_community_id = open('../data_db/community_id/110000_community_id.l', 'w', encoding='utf-8')
# 	def close_spider(self, spider):
# 		if spider.name == 'bk_bublelist':
# 			self.b420100_district.close()
# 			self.b420100_bizcircle.close()
# 			self.b420100_community.close()
# 			self.b420100_community_id.close()
# 			self.b310000_district.close()
# 			self.b310000_bizcircle.close()
# 			self.b310000_community.close()
# 			self.b310000_community_id.close()
# 			self.b110000_district.close()
# 			self.b110000_bizcircle.close()
# 			self.b110000_community.close()
# 			self.b110000_community_id.close()

# 	def process_item(self, item, spider):
# 		if spider.name == 'bk_bublelist':
# 			if item['cityId'] == '420100' and item['groupType'] == 'district':
# 				self.b420100_district.write(json.dumps(dict(item), ensure_ascii = False) + '\n')
# 			if item['cityId'] == '420100' and item['groupType'] == 'bizcircle':
# 				self.b420100_bizcircle.write(json.dumps(dict(item), ensure_ascii = False) + '\n')
# 			if item['cityId'] == '420100' and item['groupType'] == 'community':
# 				self.b420100_community.write(json.dumps(dict(item), ensure_ascii = False) + '\n')
# 				self.b420100_community_id.write(str(item['unId']) + '\n')
# 			if item['cityId'] == '310000' and item['groupType'] == 'district':
# 				self.b310000_district.write(json.dumps(dict(item), ensure_ascii = False) + '\n')
# 			if item['cityId'] == '310000' and item['groupType'] == 'bizcircle':
# 				self.b310000_bizcircle.write(json.dumps(dict(item), ensure_ascii = False) + '\n')
# 			if item['cityId'] == '310000' and item['groupType'] == 'community':
# 				self.b310000_community.write(json.dumps(dict(item), ensure_ascii = False) + '\n')
# 				self.b310000_community_id.write(str(item['unId']) + '\n')
# 			if item['cityId'] == '110000' and item['groupType'] == 'district':
# 				self.b110000_district.write(json.dumps(dict(item), ensure_ascii = False) + '\n')
# 			if item['cityId'] == '110000' and item['groupType'] == 'bizcircle':
# 				self.b110000_bizcircle.write(json.dumps(dict(item), ensure_ascii = False) + '\n')
# 			if item['cityId'] == '110000' and item['groupType'] == 'community':
# 				self.b110000_community.write(json.dumps(dict(item), ensure_ascii = False) + '\n')
# 				self.b110000_community_id.write(str(item['unId']) + '\n')
# 		return item

# class houselistPipeline(object):
# 	h420100_houselist = None
# 	h310000_houselist = None
# 	h110000_houselist = None
# 	def open_spider(self, spider):
# 		if spider.name == 'bk_houselist':
# 			self.h420100_houselist = open('../data_db/houselist/420100_houselist.jsonl', 'w', encoding='utf-8')
# 			self.h310000_houselist = open('../data_db/houselist/310000_houselist.jsonl', 'w', encoding='utf-8')
# 			self.h110000_houselist = open('../data_db/houselist/110000_houselist.jsonl', 'w', encoding='utf-8')
# 	def close_spider(self, spider):
# 		if spider.name == 'bk_houselist':
# 			self.h420100_houselist.close()
# 			self.h310000_houselist.close()
# 			self.h110000_houselist.close()
# 	def process_desc(self, item):   # 处理desc字段
# 		if '/' not in item['desc']:
# 				return item
# 		descList = item['desc'].strip().split('/')
# 		if len(descList) == 3:
# 			item['layout'], item['areaStr'], item['community'] = item['desc'].strip().split('/')
# 		elif len(descList) == 4:
# 			item['layout'], item['areaStr'], item['orientation'], item['community'] = item['desc'].strip().split('/')
# 		return item
# 	def process_someint(self, item):   # 处理priceStr、unitPriceStr、字段
# 		try:
# 			item['price'] = ''.join(str(i) for i in re.findall(r'\d+', item['priceStr']))
# 			item['unitPrice'] = ''.join(str(i) for i in re.findall(r'\d+', item['unitPriceStr']))
# 			item['area'] = re.findall(r'\d+', item['areaStr'])[0]
# 		except:
# 			item['price'] = '0'
# 			item['unitPrice'] = '0'
# 			item['area'] = '0'
# 		return item
# 	def process_item(self, item, spider):
# 		if spider.name == 'bk_houselist':
# 			item = self.process_desc(item)
# 			item = self.process_someint(item)
# 			if item['cityId'] == '420100':
# 				self.h420100_houselist.write(json.dumps(dict(item), ensure_ascii = False) + '\n')
# 			if item['cityId'] == '310000':
# 				self.h310000_houselist.write(json.dumps(dict(item), ensure_ascii = False) + '\n')
# 			if item['cityId'] == '110000':
# 				self.h110000_houselist.write(json.dumps(dict(item), ensure_ascii = False) + '\n')
# 		return item
#420100 wuhan
#110000 beijing
#310000 shanghai
class bublelistPipeline(object):
	def __init__(self):
		self.settings=get_project_settings()
		self.cityId=str(self.settings['CITY_ID'])
		self.content={}
		self.content['district']= None
		self.content['bizcircle'] = None
		self.content['community'] = None
		self.content['community_id'] = None
	def open_spider(self, spider):
		if spider.name == 'bk_bublelist':
			self.content['district']= open(f'../data_db/bublelist/{self.cityId}_district.jsonl', 'w', encoding='utf-8')
			self.content['bizcircle'] =open(f'../data_db/bublelist/{self.cityId}_bizcircle.jsonl', 'w', encoding='utf-8')
			self.content['community'] =open(f'../data_db/bublelist/{self.cityId}_community.jsonl', 'w', encoding='utf-8')
			self.content['community_id'] = open(f'../data_db/community_id/{self.cityId}_community_id.l', 'w', encoding='utf-8')
	def close_spider(self, spider):
		if spider.name == 'bk_bublelist':
			self.content['district'].close()
			self.content['bizcircle'].close()
			self.content['community'].close()
			self.content['community_id'].close()

	def process_item(self, item, spider):
		if spider.name == 'bk_bublelist':
			if item['cityId'] == self.cityId and item['groupType'] == 'district':
				self.content['district'].write(json.dumps(dict(item), ensure_ascii = False) + '\n')
			if item['cityId'] == self.cityId and item['groupType'] == 'bizcircle':
				self.content['bizcircle'].write(json.dumps(dict(item), ensure_ascii = False) + '\n')
			if item['cityId'] == self.cityId and item['groupType'] == 'community':
				self.content['community'].write(json.dumps(dict(item), ensure_ascii = False) + '\n')
				self.content['community_id'].write(str(item['unId']) + '\n')
		return item

class houselistPipeline(object):
	def __init__(self):
		self.settings=get_project_settings()
		self.cityId=str(self.settings['CITY_ID'])
		self.content={}
		self.content['houselist'] = None
	def open_spider(self, spider):
		if spider.name == 'bk_houselist':
			self.content['houselist'] = open(f'../data_db/houselist/{self.cityId}_houselist.jsonl', 'w', encoding='utf-8')
	def close_spider(self, spider):
		if spider.name == 'bk_houselist':
			self.content['houselist'].close()
	def process_desc(self, item):   # 处理desc字段
		if '/' not in item['desc']:
				return item
		descList = item['desc'].strip().split('/')
		if len(descList) == 3:
			item['layout'], item['areaStr'], item['community'] = item['desc'].strip().split('/')
		elif len(descList) == 4:
			item['layout'], item['areaStr'], item['orientation'], item['community'] = item['desc'].strip().split('/')
		return item
	def process_someint(self, item):   # 处理priceStr、unitPriceStr、字段
		try:
			item['price'] = ''.join(str(i) for i in re.findall(r'\d+', item['priceStr']))
			item['unitPrice'] = ''.join(str(i) for i in re.findall(r'\d+', item['unitPriceStr']))
			item['area'] = re.findall(r'\d+', item['areaStr'])[0]
		except:
			item['price'] = '0'
			item['unitPrice'] = '0'
			item['area'] = '0'
		return item
	def process_item(self, item, spider):
		if spider.name == 'bk_houselist':
			item = self.process_desc(item)
			item = self.process_someint(item)
			if item['cityId'] == self.cityId:
				self.content['houselist'].write(json.dumps(dict(item), ensure_ascii = False) + '\n')
		return item