import os
from time import time, ctime, sleep
from random import shuffle
from function import MongoLoadCsv
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import DataFrame as df
import urllib
import threading
import multiprocessing
from concurrent import futures
from urllib2 import Request

def getFilename(dir, results):
	
	# search_str = 'M01'
	
	folders = [dir]
	for folder in folders:
		folders += [os.path.join(folder, x) for x in os.listdir(folder) if os.path.isdir(os.path.join(folder, x))]
		
		results += [os.path.realpath(os.path.join(folder, x)) for x in os.listdir(folder)
		            if os.path.isfile(os.path.join(folder, x))]

def mongoLoadAllCsv(client, dbname, results):
	for result in results:
		path, file = os.path.split(result)
		f, ext = os.path.splitext(file)
		if ext == '.csv':
			s = f.split('_')
			agreement = s[0]
			collection = client[dbname][agreement]
			MongoLoadCsv(collection, result)
			print(result + 'have inserted')
'''
			
def read(dic):
	print('Get %s from queue.' % dic)
	

def main(results):
	futures = set()
	with futures.ThreadPoolExecutor(multiprocessing.cpu_count()*4) as executor:
		for result in results:
			future = executor.submit(read, result)
			futures.add(future)
	try:
		for future in futures.as_completed(futures):
			err = future.exception()
			if err is not None:
				raise err
			else:
				
			
	except KeyboardInterrupt:
		print("stopped by hand")

'''

def singleTh(client, dbname, dic):
	print(ctime())
	results_ = []
	getFilename(dic, results_)
	shuffle(results_)
	mongoLoadAllCsv(client, dbname, results_)

def multiTh(client, dbname, dir):
	threads = []
	for d in dir:
		t = threading.Thread(target=singleTh, args=(client, dbname, d))
		threads.append(t)
	
	for t in threads:
		t.setDaemon(True)
		t.start()
	
	for t in threads:
		t.join()


def cleardata(dbname, symbol1, symbol2, client, dataStartDate = None, dataEndDate=None, no_id=True):
	flt = {'datatime': {'$gte': dataStartDate, '$lt': dataEndDate}}
	collection1 = client[str(dbname)][str(symbol1)]
	collection2 = client[str(dbname)][str(symbol2)]
	cursor1 = collection1.find()
	cursor2 = collection2.find()
	df1 = pd.DataFrame(list(cursor1))
	df2 = pd.DataFrame(list(cursor2))
	if no_id:
		del df1['_id']
		del df2['_id']
		
	df1.sort_values('datetime', inplace='TRUE')
	print(df1)
	print(df1.describe())
	df2.sort_values('datetime', inplace='TRUE')
	print(df2)
	avg1 = df1.mean()['lastPrice']
	avg2 = df2.mean()['lastPrice']


	result1 = list(df1[df1['lastPrice'] > (avg1 / 6)]['datetime'])
	result2 = list(df2[df2['lastPrice'] > (avg2 / 6)]['datetime'])
	print(len(result1))
	print(len(result2))
	results = list(set(result1).intersection(set(result2)))
	print(len(results))
	
	data1 = df1[df1.datetime.isin(results)]
	data1.set_index('datetime', inplace='TRUE')
	data2 = df2[df2.datetime.isin(results)]
	data2.set_index('datetime', inplace='TRUE')
	print(data1,data2)
	return data1, data2

def calculate(value1,value2):
	return float(value1) - float(value2)

def calculateS(ser1, ser2, ratio1, ratio2, calculate):
	if calculate == '+':
		return ratio1 * ser1 + ser2 * ratio2
	elif calculate == '-':
		return ratio1 * ser1 - ser2 * ratio2
	elif calculate == '*':
		return ratio1 * ser1 * ser2 * ratio2
	elif calculate == '/':
		return (ratio1 * ser1) / (ser2 * ratio2)

def drawC3(data1, data2, ratio1, ratio2, calculate):
	data2.rename(columns={'lastPrice': 'lastPrice2'}, inplace=True)
	result = data1.join(data2)
	
	c = calculateS(result['lastPrice'], result['lastPrice2'], ratio1, ratio2, calculate)
	f_data = pd.DataFrame(c, columns=['value'])

	max_value = max(f_data['value'])
	min_value = min(f_data['value'])
	avg_value = f_data.mean()
	print('max_value:%d' % max_value)
	print('min_value:%d' % min_value)
	print('avg_value:%d' % avg_value)
	return f_data, max_value, min_value, avg_value

def show(f_data):
	f_data.plot()
	#plt.annotate('max_value', xy=(f_data.idxmax()['value'], max_value),
	            # xytext=(f_data.idxmax()['value'], max_value + 200), arrowprops=dict(facecolor='black', shrink=0.1))
	
	#plt.text(f_data.first_valid_index(), min_value, 'min_value:%d' % min_value)
	#plt.text(f_data.first_valid_index(), min_value+100, 'max_value:%d' % max_value)
	#plt.legend(loc='best')

	plt.show()
	#plt.plot(x, y)

	#plt.show()

def drawC2(data1, data2):
	data2.rename(columns={'lastPrice': 'lastPrice2'}, inplace=True)
	result = data1.join(data2)
	x = []
	y = []
	start = time()
	for index, row in result.iterrows():
		value = calculate(row['lastPrice'], row['lastPrice2'])
		x.append(index)
		y.append(value)
	print(x, y)
	#plt.plot(x, y)
	print(u'Completed,consuming time:%s' % (time() - start))
	plt.show()

def drawC(data1, data2):
	data2.rename(columns={'doubleValue': 'dv2', 'lastPrice': 'lp2'}, inplace=True)
	result = data1.join(data2)
	x = []
	y = []
	start = time()
	print(result['lastPrice'][0])
	for index, row in result.iterrows():
		if row['doubleValue'] and row['dv2']:
			lastprice1 = (float(row['lastPrice'][0])+float(row['lastPrice'][1]))/2
			lastprice2 = (float(row['lp2'][0]) + float(row['lp2'][1])) / 2
			
		else:
			lastprice1 = row['lastPrice'][0]
			lastprice2 = row['lp2'][0]
		value = calculate(lastprice1, lastprice2)
		x.append(index)
		y.append(value)
	plt.plot(x, y)
	print(u'Completed,consuming time:%s' % (time() - start))
	plt.show()
	
if __name__ == '__main__':
	start = time()
	#results.clear()
	
	host, port = 'localhost', 27017
	client = pymongo.MongoClient(host, port)
	dbname = 'mainT2'
	#multiTh(client, dbname, dir)
	data1, data2 = cleardata(dbname, 'RB10', 'I09', client)
	drawC3(data1, data2)
	#drawC1(dbname, 'M05', 'SRY05', client)

	print(u'Completed,consuming time:%s' % (time() - start))

