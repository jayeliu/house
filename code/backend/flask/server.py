#### --------slight flask server
from flask import Flask, request, session
from flask import jsonify
from flask_cors import CORS
# import utils.sqlDB as sqlDB
from utils.utils import GetOutlineSrc, ParseJson, LoadLocalJsonl, RunScrapy, overSpace, pagination, dfQueryKey, dfQueryParams
import argparse

parser = argparse.ArgumentParser(description='命令行中服务器IP')
#type是要传入的参数的数据类型  help是该参数的提示信息
parser.add_argument('--ip', type=str, help='ip addr',default='localhost')
parser.add_argument('--port', type=str, help='binding port',default='8083',required=False)
args = parser.parse_args()

### =========================== utils ===========================


## --------数据库
# def fetchDb(myDB):
# 	print (myDB.showSQL('show tables;'))
# 	print(myDB.FieldType('CITY_ID','bs_city'))
# 	# sqlDB.queryBy()
# 	myDB.exit()


### =========================== flask ===========================

app = Flask(__name__)
app.secret_key = '123456'
# session.permanent = True
# app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)
# 配置允许跨域源
cors = CORS(app, resources={
	r"/addressSelection": {"origins": "*"},
	r"/geoCoding": {"origins": "*"},
	r"/bublelist": {"origins": "*"},
	r"/houselist": {"origins": "*"},
	})
# myDB = sqlDB.fetchFromDB()
@app.route('/index',methods=['GET'])
def index():
	return "<h1>Hello World</h1>"


# **** 地址选择 /addressSelection?code=
@app.route('/addressSelection',methods=['GET'])
def addressSelection():
	regionCodeStr = request.args.get('code')
	if not (regionCodeStr):
		return ""
	regionCodes = regionCodeStr.split(",")
	jsonObject = []
	for regionCode in regionCodes:
		# 顺丰外部接口
		url = f"https://www.sf-express.com/sf-service-owf-web/service/region/new/{regionCode}/subRegions?lang=sc&region=cn"
		jsonObject += (ParseJson(GetOutlineSrc(url)))
	return jsonify(jsonObject)

# **** 地址编码 /geoCoding?address= &ak= 
@app.route('/geoCoding',methods=['GET'])
def geoCoding():
	address = request.args.get('address')
	ak = request.args.get('ak')
	city = request.args.get('city')
	ret_coordtype = request.args.get('ret_coordtype')
	
	# baidu api
	url = f"http://api.map.baidu.com/geocoding/v3/?address={address}&output=json&ak={ak}&city={city}&ret_coordtype={ret_coordtype}"
	return jsonify(ParseJson(GetOutlineSrc(url)))

# **** 房源信息bublelist /bublelist?cityId= &groupType=
@app.route('/bublelist',methods=['GET'])
def bublelist():
	cityId = request.args.get('cityId')
	groupType = request.args.get('groupType')
	jsonlFile = f'bublelist/{cityId}_{groupType}.jsonl'
	jsonObject = LoadLocalJsonl(jsonlFile)
	response = jsonify(jsonObject)
	# session['scrapyTime'] = overSpace('bk_bublelist', session.get('scrapyTime'))   # 触发定时Scrapy爬虫
	return response

# **** 房源信息houselist /houselist?cityId= &resblockId= 
@app.route('/houselist',methods=['GET'])
def houselist():
	cityId = request.args.get('cityId')
	resblockId = request.args.get('resblockId')
	currentPage = request.args.get('currentPage')
	pageSize = request.args.get('pageSize')
	queryKey = request.args.get('queryKey')
	queryParams = request.args.get('queryParams')
	jsonlFile = f'houselist/{cityId}_houselist.jsonl'
	jsonObject = LoadLocalJsonl(jsonlFile)
	if queryKey:
		jsonObject = dfQueryKey(jsonObject, queryKey)
	if queryParams and len(jsonObject) != 0:
		jsonObject = dfQueryParams(jsonObject, ParseJson(queryParams))
	if resblockId:
		jsonObject_res = []
		for jsonObject_dict in jsonObject:
			if jsonObject_dict['resblockId'] == resblockId:
				jsonObject_res.append(jsonObject_dict)
		jsonObject = jsonObject_res
	jsonObject = pagination(jsonObject, currentPage, pageSize)
	response = jsonify(jsonObject)
	# session['scrapyTime'] = overSpace('bk_houselist', session.get('scrapyTime'))   # 定时爬虫
	return response

### =========================== runing ===========================
if __name__ == '__main__':
    app.run(host=args.ip, port =args.port)