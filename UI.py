import sys
import pymongo
import time
from datetime import datetime
from PyQt4.QtGui import (QApplication, QLabel, QComboBox, QTextEdit, QDateTimeEdit, QGridLayout, QWidget, QLineEdit, QDesktopWidget, QAction, qApp, QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QPushButton)
from PyQt4.QtGui import QIcon
from PyQt4.QtCore import QDateTime
from PyQt4.QtCore import QThread
from PyQt4 import QtCore
import threading
from all_setting import catalog, dataEndDate, dataStartDate, dbName, agreement1, agreement2
from test3 import cleardata, drawC3, show

class WorkThread(QThread):
	finishSignal = QtCore.pyqtSignal(list)
	def __init__(self,agreement1ID, agreement2ID, startTime, endTime, c1, c3, calculate1):
		QThread.__init__(self)
		self.dbNameInit = 'test1'
		self.agreement1ID=agreement1ID
		self.agreement2ID=agreement2ID
		self.startTime=startTime
		self.endTime=endTime
		self.c1=c1
		self.c3=c3
		self.calculate1=calculate1

	def run(self):
		host, port = 'localhost', 27017
		client = pymongo.MongoClient(host, port)
		data1, data2 = cleardata(self.dbNameInit, self.agreement1ID, self.agreement2ID, client, self.startTime, self.endTime)
		f_data, max_v, min_v, avg = drawC3(data1, data2, float(self.c1), float(self.c3), self.calculate1)
		#self.stateEdit.append(u'Maximum:%f' % max_v)
		#self.stateEdit.append(u'Minimum:%f' % min_v)
		#self.stateEdit.append(u'Average:%f' % avg)
		#show(f_data)
		self.finishSignal.emit([f_data, max_v, min_v, avg])


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow,self).__init__()
		self.agreement1ID = 'AG01'
		self.agreement2ID = 'AG02'
		self.dbNameInit = 'test1'
		self.calculate1 = '+'
		self.c1 = '1'
		self.c3 = '1'
		self.threads = []
		self.onInit()
		
		
	def onInit(self):
		self.resize(450, 300)
		self.center()
		self.setMenu()
		self.setWindowTitle(u'MainWindow')
		self.setWindowIcon(QIcon('learning.ico'))
		
		self.agreement1 = QLabel('Contract1', self)
		self.agreement11 = QLabel('      Contract1 *', self)
		
		self.agreement2 = QLabel('Contract2', self)
		self.agreement22 = QLabel('Contract2 *', self)
		self.calculate = QLabel('Formula', self)
		self.startTime = QLabel('Start Time', self)
		self.endTime = QLabel('End Time', self)
		self.agreement1Edit = QLineEdit()
		self.agreement2Edit = QLineEdit()
		self.calculate1Edit = QLineEdit()
		self.calculate2Combo = QComboBox()
		self.calculate2Combo.addItem('+')
		self.calculate2Combo.addItem('-')
		self.calculate2Combo.addItem('*')
		self.calculate2Combo.addItem('/')
		
		self.calculate2Combo.activated[str].connect(self.onActivated)
		
		self.calculate2Edit = QLineEdit()
		self.calculate3Edit = QLineEdit()
		self.startTimeEdit = QDateTimeEdit(datetime.strptime('20150101 00:00:00', '%Y%m%d %H:%M:%S'), self)
		self.startTimeEdit.setDisplayFormat('yyyy-MM-dd')
		self.startTimeEdit.setCalendarPopup(True)
		self.endTimeEdit = QDateTimeEdit(QDateTime.currentDateTime(), self)
		self.endTimeEdit.setDisplayFormat('yyyy-MM-dd')
		self.endTimeEdit.setCalendarPopup(True)
		self.stateEdit = QTextEdit()
		
		self.run = QPushButton('Run', self)
		self.run.clicked.connect(self.runMain)
		self.clearEdit = QPushButton('Clear', self)
		self.clearEdit.clicked.connect(self.clearEdition)
		#self.setAgreementBtn = QPushButton('Setting', self)
		#self.setAgreementBtn.clicked.connect(self.setAgreement)
		
		grid = QGridLayout()
		#grid.setSpacing(10)
		grid.addWidget(self.agreement1, 1, 0)
		grid.addWidget(self.agreement1Edit, 1, 1)
		grid.addWidget(self.agreement2, 2, 0)
		grid.addWidget(self.agreement2Edit, 2, 1)
		#grid.addWidget(self.setAgreementBtn, 2, 2)
		grid.addWidget(self.startTime, 3, 0)
		grid.addWidget(self.startTimeEdit, 3, 1)
		grid.addWidget(self.endTime, 4, 0)
		grid.addWidget(self.endTimeEdit, 4, 1)
		grid.addWidget(self.calculate, 5, 0)
		grid.addWidget(self.agreement11, 5, 1)
		grid.addWidget(self.calculate1Edit, 5, 2)
		grid.addWidget(self.calculate2Combo, 5, 3)
		grid.addWidget(self.agreement22, 5, 4)
		grid.addWidget(self.calculate3Edit, 5, 5)
		grid.addWidget(self.stateEdit, 6, 1, 1, 5)
		grid.addWidget(self.run, 7, 1)
		grid.addWidget(self.clearEdit, 7, 2)
		gridWidget = QWidget()
		gridWidget.setLayout(grid)
		self.agreement11.move(200, 100)
		self.setCentralWidget(gridWidget)
		self.show()
	
	def clearEdition(self):
		self.stateEdit.clear()
		
	def onActivated(self, text):
		self.calculate1 = text
	
	def setMenu(self):
		exitAction = QAction(u'Quit', self)
		exitAction.triggered.connect(qApp.quit)
		
		menubar = self.menuBar()
		fileMenu = menubar.addMenu(u'Menu')
		fileMenu.addAction(exitAction)
	
	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def done(self,ls):
		self.stateEdit.append(u'Maximum:%f' % ls[1])
		self.stateEdit.append(u'Minimum:%f' % ls[2])
		self.stateEdit.append(u'Average:%f' % ls[3])
		show(ls[0])
		self.run.setEnabled(True)
		self.stateEdit.append('End time: %s' % time.ctime())

	def runMain(self):
		self.run.setEnabled(False)
		agreementt1 = self.agreement1Edit.text()
		agreementt2 = self.agreement2Edit.text()
		if agreementt1 == '':
			self.stateEdit.append('Settings of contract1 have error!')
		elif agreementt2 == '':
			self.stateEdit.append('Settings of contract2 have error!')
		else:
			self.agreement1ID = agreementt1
			self.agreement2ID = agreementt2
		startTime = self.startTimeEdit.dateTime()
		endTime = self.endTimeEdit.dateTime()
		self.c1 = self.calculate1Edit.text()
		self.c3 = self.calculate3Edit.text()
		self.stateEdit.append('Formula:'+self.c1+'*' + self.agreement1ID + self.calculate1 + self.c3 + '*' + self.agreement2ID)
		self.stateEdit.append('Contract1:' + self.agreement1ID + ' Contract2:' + self.agreement2ID + '  have set')
		self.stateEdit.append('Start time: %s' % time.ctime())
		self.workThread=WorkThread(self.agreement1ID,self.agreement2ID,startTime, endTime, self.c1, self.c3, self.calculate1)
		self.workThread.finishSignal.connect(self.done)
		self.workThread.start()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())
