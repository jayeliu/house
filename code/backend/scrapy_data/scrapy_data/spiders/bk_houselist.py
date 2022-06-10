# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_data.items import houslistItem
import logging
from scrapy.utils.project import get_project_settings
settings=get_project_settings()
cityId=str(settings['CITY_ID'])
class BkHouselistSpider(scrapy.Spider):
	name = "bk_houselist"
	allowed_domains = ["ke.com"]
	base_url = 'https://map.ke.com/proxyApi/i.c-pc-webapi.ke.com/map/houselist'
	def start_requests(self):
		cityId_2_lat_lng = {
			'420100':['32','29','116','113'],  # wuhan
			'310000':['32','30','123','120'],   # shanghai
			'110000':['41.6','39.4','117.4','115.7']# beijing 
			}
		groupTypes = ['district','bizcircle','community']
		lat_lng=cityId_2_lat_lng[cityId]
		with open(f'../data_db/community_id/{cityId}_community_id.l') as rfId:
			resblockIds = rfId.readlines()
			for resblockIde in resblockIds:
				resblockId = resblockIde.strip()
				params = {
					'cityId': cityId,
					'dataSource': 'ESF',
					'curPage': '1',
					'condition': '',
					'type': '',
					'resblockId': resblockId,
					'maxLatitude': lat_lng[0],
					'minLatitude': lat_lng[1],
					'maxLongitude': lat_lng[2],
					'minLongitude': lat_lng[3],
					}
				yield scrapy.FormRequest(
					url = self.base_url, 
					callback = self.parse_houselist, 
					method = 'GET',
					formdata = params,
					meta = {'params': params}
					)

	def setHouselistItem(self, item, data, cityId, resblockId):
		item['title'] = data['title']
		item['desc'] = data['desc']
		item['cityId'] = cityId
		item['resblockId'] = resblockId
		item['coverPic'] = data['coverPic']
		item['priceStr'] = data['priceStr']
		item['unitPriceStr'] = data['unitPriceStr']
		item['cardType'] = data['cardType']
		item['actionUrl'] = data['actionUrl']

	def parse_houselist(self, response):
		cityId, resblockId = response.meta['params']['cityId'], response.meta['params']['resblockId']
		BkHouseObj = json.loads(response.text)
		if BkHouseObj['errno']:
			errmsg = BkHouseObj['errmsg']
			logging.error(f' Spidering houselist:{ cityId }_{ resblockId } \n Errmsg:{ errmsg } ')
			return
		dataAll = BkHouseObj['data']
		hasMore = dataAll['hasMore']
		if not hasMore:
			return
		params = response.meta['params']
		params['curPage'] = str(int(response.meta['params']['curPage'])+1)
		yield scrapy.FormRequest(
			url = self.base_url, 
			callback = self.parse_houselist, 
			method = 'GET',
			formdata = params,
			meta = {'params': params}
			)
		total = dataAll['total']
		logging.info(f' Spidering houselist:{ cityId }_{ resblockId } \n Total:{ total }')
		dataList = dataAll['list']
		for data in dataList:
			item = houslistItem()
			self.setHouselistItem(item, data, cityId, resblockId)
			yield item