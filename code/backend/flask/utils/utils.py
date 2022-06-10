from tkinter.messagebox import NO
from pyparsing import null_debug_action
import requests
import json
import os
import datetime
import _thread
import pandas as pd
## --------requests获取外网数据
def GetOutlineSrc(url):
	try:
		r=requests.get(url)
		r.raise_for_status()
		r.encoding='utf-8'
		if (".jpg"  in url) or (".jpeg" in url) :
			return r.content
		else :
			return r.text
	except Exception as e:
		# logger.error(e)
		return ""
## --------解析爬取的json转为list
def ParseJson(jsonString):
	try:
		jsonObject = json.loads(jsonString)
	except Exception as e:
		# app.logger.error(e)
		jsonObject = []
	return jsonObject
## --------读取本地jsonl
def LoadLocalJsonl(jsonlFile):
	jsonObject = []
	try:
		with open('../data_db/'+jsonlFile,'r',encoding = 'utf-8') as rdJsonl:
			for jsonlStr in rdJsonl.readlines():
				jsonObject.append(json.loads(jsonlStr))
	except Exception as e:
		# app.logger.error(e)
		jsonObject = []
	return jsonObject
## --------执行scrapy更新数据
def RunScrapy(spidername):
	print('-'*20+'scrapying'+'-'*20)
	cmd1 = 'cd ../scrapy_data'
	cmd2 = f'scrapy crawl {spidername} --nolog'
	cmd = cmd1 + " && " + cmd2
	print(cmd)
	os.system(cmd)
## --------指定请求时间间隔执行(请求时间间隔大于10分钟，更新本地数据)
def overSpace(spidername, scrapyTime):
	timenowStr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
	timenow = int(timenowStr)
	if scrapyTime :
		space = timenow - scrapyTime
		if space < 3000:
			return scrapyTime
	_thread.start_new(RunScrapy,(spidername,))
	return timenow
## --------分页
def pagination(jsonObject, currentPageStr, pageSizeStr):
	if currentPageStr.isdigit():
		currentPage = int(currentPageStr)
	else:
		currentPage = 10000000
	if pageSizeStr.isdigit():
		pageSize = int(pageSizeStr)
	else:
		pageSize = 10000000
	pageJsonObject = {"currentPage": currentPage, "pageSize": pageSize, "pageCount":1, "data": []}
	if len(jsonObject) <= pageSize:
		if currentPage == 1:
			pageJsonObject["data"] = jsonObject
	else:
		pageJsonObject["pageCount"] = int(len(jsonObject)/pageSize)+1
		pageJsonObject["data"] = jsonObject[(currentPage-1)*pageSize:currentPage*pageSize]
	return pageJsonObject
## --------pandas关键字查询
def dfQueryKey(dfObject, queryKey):
	df = pd.DataFrame(dfObject)
	df = df.loc[df['title'].str.contains(queryKey)|
	df['priceStr'].str.contains(queryKey)|
	df['desc'].str.contains(queryKey)|
	df['unitPriceStr'].str.contains(queryKey)
	]
	jsonStr = df.to_json(orient='index')
	jsonObject = json.loads(jsonStr).values()
	return list(jsonObject)
## --------pandas参数查询
def dfQueryParams(dfObject, queryParams):
	df = pd.DataFrame(dfObject)
	df[['price','unitPrice','area']] = df[['price','unitPrice','area']].astype(int)
	if 'layout' in queryParams:
		if queryParams['layout'] != []:
			df = df.loc[df['layout'].isin(queryParams['layout'])]
	if 'cardType' in queryParams:
		if queryParams['cardType'] != []:
			df = df.loc[df['cardType'].isin(queryParams['cardType'])]
	df = df.loc[(df['price']>=int(queryParams['priceRange'][0]))&(df['price']<=int(queryParams['priceRange'][1]))]
	df = df.loc[(df['unitPrice']>=int(queryParams['unitPriceRange'][0]))&(df['unitPrice']<=int(queryParams['unitPriceRange'][1]))]
	df = df.loc[(df['area']>=int(queryParams['areaRange'][0]))&(df['area']<=int(queryParams['areaRange'][1]))]
	jsonStr = df.to_json(orient='index')
	jsonObject = json.loads(jsonStr).values()
	return list(jsonObject)
