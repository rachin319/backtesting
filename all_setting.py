# encoding: UTF-8

import os
import json
from datasetting import *

# 目录名
catalog = ''
# 数据库名
dbName = ''
# 连接名
agreement1 = ''
agreement2 = ''
# 文件结果集
results = []
# 数据开始时间
dataStartDate = None
# 数据结束时间
dataEndDate = None

# 默认空值
EMPTY_STRING = ''
EMPTY_UNICODE = u''
EMPTY_INT = 0
EMPTY_FLOAT = 0.0

"""
包含一些基础的类
"""
class Temp(object):
	def __init__(self):
		self.datetime = None
		self.lastPrice = [0.0, 0.0]
		self.doubleValue = False




def loadMongoSetting():
	"""载入MongoDB数据库的配置"""
	fileName = 'setting.json'
	path = os.path.abspath(os.path.dirname(__file__))
	fileName = os.path.join(path, fileName)
	
	try:
		f = open(fileName)
		setting = json.load(f)
		host = setting['mongoHost']
		port = setting['mongoPort']
	except:
		host = 'localhost'
		port = 27017
	
	return host, port


class TickData(object):
	"""Tick数据"""
	# ----------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""
		# self.symbol = EMPTY_STRING  # 合约代码
		# 成交数据
		# self.openInterest = EMPTY_INT  # 持仓量
		# self.upperLimit = EMPTY_FLOAT  # 涨停价
		# self.lowerLimit = EMPTY_FLOAT  # 跌停价
		# tick的时间
		self.date = EMPTY_STRING  # 日期
		self.time = EMPTY_STRING  # 时间
		self.datetime = None  # python的datetime时间对象
		
		self.doubleValue = False
		# value
		# self.bidPrice1 = [0.0, 0.0]
		# self.askPrice1 = [0.0, 0.0]
		# self.bidVolume1 = [0, 0]
		# self.askVolume1 = [0, 0]
		self.lastPrice = [0.0, 0.0]  # 最新成交价
		# self.volume = [0, 0]  # 最新成交量

