# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_data.items import bublelistItem
import logging
from scrapy.utils.project import get_project_settings
settings=get_project_settings()
cityId=str(settings['CITY_ID'])
class BkBublelistSpider(scrapy.Spider):
	name = "bk_bublelist"
	allowed_domains = ["ke.com"]
	base_url = 'https://map.ke.com/proxyApi/i.c-pc-webapi.ke.com/map/bubblelist'
	def start_requests(self):
		cityId_2_lat_lng = {
			'420100':['30.69','30.60','114.65','113.96'],  # wuhan
			'310000':['32','30','123','120'],   # shanghai
			'110000':['41.6','39.4','117.4','115.7']   # shanghai
			}
		groupTypes = ['district','bizcircle','community']
		lat_lng=cityId_2_lat_lng[cityId]
		for groupType in groupTypes:
			params = {
				'cityId': cityId,
				'dataSource': 'ESF',
				'condition': '',
				'id': '',
				'groupType': groupType,
				'maxLatitude': lat_lng[0],
				'minLatitude': lat_lng[1],
				'maxLongitude': lat_lng[2],
				'minLongitude': lat_lng[3],
				}
			yield scrapy.FormRequest(
				url = self.base_url, 
				callback = self.parse_publelist, 
				method = 'GET',
				formdata = params,
				meta = {'params': params}
				)
	# def latAndLng():
	# 	lat_lng = [str(l1),str(l2),str(l3),str(l4)]
	# 	l1 = l1-0.04
	# 	l2 = l1-0.08
	# 	l3 = l3-0.05
	# 	l4 = l4-0.10
	# 	if l2<30.16&l4<113.46:
	# 		return
	def setBublelistItem(self, item, data, cityId, groupType):
		item['unId'] = data['id']
		item['name'] = data['name']
		item['cityId'] = cityId
		item['groupType'] = groupType
		item['count'] = data['count']
		item['countUnit'] = data['countUnit']
		item['price'] = data['price']
		item['priceUnit'] = data['priceUnit']
		item['border'] = data['border']
		item['lng'] = data['longitude'] 
		item['lat'] = data['latitude']

	def parse_publelist(self, response):
		cityId, groupType = response.meta['params']['cityId'], response.meta['params']['groupType']
		BkBubleObj = json.loads(response.text)
		if BkBubleObj['errno']:
			errmsg = BkBubleObj['errmsg']
			logging.error(f' Spidering bubblelist:{ cityId }_{ groupType } \n Errmsg:{ errmsg } ')
			return
		dataAll = BkBubleObj['data']
		totalCount = dataAll['totalCount']
		logging.info(f' Spidering bubblelist:{ cityId }_{ groupType } \n TotalCount:{ totalCount }')
		dataList = dataAll['bubbleList'] 
		for data in dataList:
			item = bublelistItem()
			self.setBublelistItem(item, data, cityId, groupType)
			yield item
