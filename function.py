import os
from datetime import datetime
import csv
from all_setting import TickData
import pymongo
from all_setting import loadMongoSetting


def clearDatatoSame(dbname1, dbname2, symbol1, symbol2):
	host, port = loadMongoSetting()
	dbclient = pymongo.MongoClient(host, port)
	
	collection1 = dbclient[dbname1][symbol1]
	collection1.ensure_index([('datetime', pymongo.ASCENDING)], unique=True)
	collection2 = dbclient[dbname2][symbol2]
	collection2.ensure_index([('datetime', pymongo.ASCENDING)], unique=True)
	# flt = {'datatime': {'$gte': dataStartDate, '$lt': dataEndDate}}
	
	cursor = collection1.find()
	results1 = []
	for d in cursor:
		results1.append(d['datetime'])
	cursor = collection2.find()
	results2 = []
	for d in cursor:
		results2.append(d['datetime'])
	results = list(set(results1).intersection(set(results2)))
	res1 = list(set(results1).difference(set(results)))
	res2 = list(set(results2).difference(set(results)))
	for res in res1:
		collection1.remove({'datetime': res})
	for res in res2:
		collection2.remove({'datetime': res})


def MongoLoadCsv1(collection, filename):
	reader = csv.DictReader(open(filename, 'r'))
	lastdatetime = None
	temp_list = []
	for d in reader:
		temp = {'lastPrice': [0.0, 0.0], 'doubleValue': False, 'datetime': None}
		date = datetime.strptime(d['Time'], '%Y-%m-%d').strftime('%Y%m%d')
		time = datetime.strptime(d['Date'], '%H:%M:%S').strftime('%H:%M:%S')
		temp['datetime'] = datetime.strptime(date + ' ' + time, '%Y%m%d %H:%M:%S')
		i = 0
		if lastdatetime != temp['datetime']:
			temp['lastPrice'][i] = d['lastPrice']
			temp_list.append(temp)
			lastdatetime = temp['datetime']
		else:
			temp1 = temp_list.pop()
			i = 1
			temp1['doubleValue'] = True
			temp1['lastPrice'][i] = d['lastPrice']
			temp_list.append(temp1)
			lastdatetime = temp1['datetime']
	collection.insert(temp_list)

def MongoLoadCsv(collection, filename):
	reader = csv.DictReader(open(filename, 'r'))
	lastdatetime = None
	temp_list = []
	for d in reader:
		temp = {'lastPrice': 0.0, 'datetime': None}
		date = datetime.strptime(d['Time'], '%Y-%m-%d').strftime('%Y%m%d')
		time = datetime.strptime(d['Date'], '%H:%M:%S').strftime('%H:%M:%S')
		temp['datetime'] = datetime.strptime(date + ' ' + time, '%Y%m%d %H:%M:%S')
		if lastdatetime != temp['datetime']:
			temp['lastPrice'] = float(d['lastPrice'])
			temp_list.append(temp)
			lastdatetime = temp['datetime']
		else:
			temp1 = temp_list.pop()
			t = temp1['lastPrice']
			temp1['lastPrice']= (float(t)+float(d['lastPrice']))/2
			temp_list.append(temp1)
			lastdatetime = temp1['datetime']
	collection.insert(temp_list)

# def mongoLoadAllCsv(collection):
	

def getFilename(dir, results, search_str, nothave_str='*'):

	results.clear()
	folders = [dir]
	for folder in folders:
		folders += [os.path.join(folder, x) for x in os.listdir(folder) if os.path.isdir(os.path.join(folder, x))]
		if nothave_str !='*':
			results += [os.path.realpath(os.path.join(folder, x)) for x in os.listdir(folder)
						if os.path.isfile(os.path.join(folder, x)) and search_str in x and nothave_str not in x]
		else:
			results += [os.path.realpath(os.path.join(folder, x)) for x in os.listdir(folder)
						if os.path.isfile(os.path.join(folder, x)) and search_str in x]

														
if __name__ == '__main__':
	host, port = loadMongoSetting()
	client = pymongo.MongoClient(host, port)
	collection1 = client['main']['M01']
	collection1.ensure_index([('datetime', pymongo.ASCENDING)], unique=True)
	collection2 = client['main']['M05']
	collection2.ensure_index([('datetime', pymongo.ASCENDING)], unique=True)
	MongoLoadCsv(collection1, 'M01_20160516.csv')
	MongoLoadCsv(collection2, 'M05_20160516.csv')
	
	clearDatatoSame('main', 'main', 'M01', 'M05')
	''''''
