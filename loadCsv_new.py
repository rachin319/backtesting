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
def loadCsv(filename, dbName, symbol):
	
	#print u'Start'

	host, port, logging = loadMongoSetting()
	#print host, port

	client = pymongo.MongoClient(host,port)
	collection = client[dbName][symbol]
	collection.ensure_index([('datetime', pymongo.ASCENDING)],unique=True)
	reader = csv.reader(file(filename,'r'))
	first_line = True
	lastdatetime = None
	temp_list=[]
	for d in reader:
		try:
			if first_line or d[6]=='0' or d[7]=='0' or d[12]=='0' or d[13]=='0':
				first_line = False
				continue
		except IndexError:
			break
		temp = {'lastPrice': 0.0, 'datetime':None}
		date=datetime.strptime(d[0], '%Y-%m-%d').strftime('%Y%m%d')
		time=datetime.strptime(d[1], '%H:%M:%S').strftime('%H:%M:%S')
		temp['datetime'] = datetime.strptime(date + ' ' + time, '%Y%m%d %H:%M:%S')
		if lastdatetime != temp['datetime']:
			temp['lastPrice'] = float(d[2])
			temp_list.append(temp)
			lastdatetime = temp['datetime']
		else:
			temp1 = temp_list.pop()
			t = temp1['lastPrice']
			temp1['lastPrice']= (float(t)+float(d[2]))/2
			temp_list.append(temp1)
			lastdatetime = temp1['datetime']
		#print temp['datetime']
	try:
		collection.insert(temp_list)
		print u'OK', filename
	except:
		for i in temp_list:
			try:
				collection.insert([i])
				print u'OK',i['datetime']
			except:
				print u'Fail',i['datetime']
				continue

if __name__=='__main__':
	root = Tkinter.Tk()
	root.withdraw()
	directory=tkFileDialog.askdirectory(parent=root,title='Pick a directory')
	filenames = getFilename(directory)
	#print len(filenames)
	#for i in range(13, 14):
	for i in range(len(filenames)):
		coll = getCollectionName(filenames[i])
		loadCsv(filenames[i], 'test1', coll)
