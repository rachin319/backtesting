#coding:utf-8
#__author__ = 'rachin'

import sys
sys.path.append('/home/vnpy/vnpy/vn.trader')			#使用时需更改为对应的本地文件夹
sys.path.append('/home/vnpy/vnpy/vn.trader/ctaAlgo')	#使用时需更改为对应的本地文件夹
reload(sys)  
sys.setdefaultencoding('utf8')   
import os
import re

from datetime import datetime, timedelta
import pymongo
import csv
from time import time
from multiprocessing.pool import ThreadPool
import Tkinter, tkFileDialog

from ctaBase import *
from vtConstant import *
from vtFunction import loadMongoSetting
from datayesClient import DatayesClient

#test_file = u"/home/vnpy/文档/20160104/AX01_20160104.csv"

#获取dirname目录下的所有csv文件名
def getFilename(dirname):
	filenames=[]
	pattern = re.compile(r'.*\.csv')
	for dirpath, dirname, filename in os.walk(dirname):
		for f in filename:
			if pattern.match(f) is not None:
				filenames.append(str(dirpath+'/'+f))
	return filenames

#获取合约代码
def getCollectionName(filename):
	#print filename
	#print filename.split('/')[-1].split('_')[0]
	return filename.split('/')[-1].split('_')[0]

#将Csv文件中的内容载入Mongdb
def loadCsv(filename, dbName, symbol, exch):
	start = time()
	#print u'Start'

	host, port = loadMongoSetting()
	#print host, port

	client = pymongo.MongoClient(host,port)
	collection = client[dbName][symbol]
	collection.ensure_index([('datetime', pymongo.ASCENDING)],unique=True)
	reader = csv.reader(file(filename,'r'))
	first_line = True
	for d in reader:
		try:
			if first_line or d[6]=='0' or d[7]=='0' or d[12]=='0' or d[13]=='0':
				first_line = False
				continue
		except IndexError:
			break
		tick = CtaTickData()
		tick.vtSymbol = symbol
		tick.symbol = symbol
		tick.exchange = exch
		tick.lastPrice = float(d[2])
		tick.volume = float(d[3])
		tick.openInterest=float(d[5])
		tick.date=datetime.strptime(d[0], '%Y-%m-%d').strftime('%Y%m%d')
		tick.time=d[1]
		tick.datetime = datetime.strptime(tick.date+' '+tick.time, '%Y%m%d %H:%M:%S')

		tick.bidPrice1=float(d[12])
		#tick.bidPrice2=float(d[14])
		#tick.bidPrice3=float(d[16])

		tick.askPrice1=float(d[6])
		#tick.askPrice2=float(d[8])
		#tick.askPrice3=float(d[10])

		tick.bidVolume1=float(d[13])
		#tick.bidVolume2=float(d[15])
		#tick.bidVolume3=float(d[17])

		tick.askVolume1=float(d[7])
		#tick.askVolume2=float(d[9])
		#tick.askVolume3=float(d[11])

		flt = {'datetime' : tick.datetime}
		collection.update_one(flt, {'$set':tick.__dict__}, upsert=True)
		print symbol, tick.date, tick.time
	print u'OK', filename

if __name__=='__main__':
	root = Tkinter.Tk()
	root.withdraw()
	directory=tkFileDialog.askdirectory(parent=root,title='Pick a directory')
	filenames = getFilename(directory)
	#print len(filenames)
	for i in range(13, 14):
	#for i in range(len(filenames)):
		coll = getCollectionName(filenames[i])
		loadCsv(filenames[i], 'test1', coll, 'DL')
