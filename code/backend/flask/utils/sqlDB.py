import pymysql
import pandas as pd

# 链接数据库
class fetchFromDB:
	def __init__(self):
		self.engineDb = pymysql.connect(
		host='192.168.***.***',
		port=****,
		user='user1',
		password='***',
		db='house_selection_db',
		charset='utf8',
		)
		self.cursor = self.engineDb.cursor()
	def showSQL(self, sql):
		try:
			return pd.read_sql_query(sql, self.engineDb)
		except Exception as e:
			print(e)
			return
	def exeSQL(self, sql):
		try:
			self.cursor.execute(sql)
			print('SQL done!')
		except Exception as e:
			print(e)
		return
	def FieldType(self, field, table):
		SQLcmd = f'''SHOW full columns FROM {table} LIKE '{field}';'''
		fieldAttrs = self.showSQL(SQLcmd)
		return fieldAttrs['Type']
	def exit(self):
		self.cursor.close()
		self.engineDb.close()

# sql查询
class queryBy(fetchFromDB):
	def __init__(self, queryParams, table):
		if not isinstance(queryParams, dict):
			return
		SQLcmd_base = f'''SELECT * FROM {table} WHERE '''
		for queryField, queryValue in queryParams.items():
			SQLcmd_where_single = '''
			{queryField}=\'{queryValue}\'
			'''