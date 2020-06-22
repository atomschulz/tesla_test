import pyodbc #Python Open Database connector is used to connect to Microsoft SQL database
import pandas as pd #Pandas is used for is class dataframe which is hugely useful for indexing large datasets
import os #to check if certain files exist
import numpy as np #on rare occassion for matrix operations manipulating the data at large.
from datetime import datetime
from pathlib import Path
import os
import time
import datetime
import smtplib
import ast

class take_home():

	#initialization of take home test class
	def __init__(self):
		#Base path of script
		self.BASEPATH = Path(__file__).parents[0]

		#parent folder
		self.parentPath = Path(__file__).parents[1]

		#data folder name
		self.dataFolder = "data"
		#name of csv1
		self.modelPath = "models.csv"
		#name of csv2
		self.plansPath = "plans.csv"
		#name of csv3
		self.shipmentsPath = "shipments.csv"

		#sqllite database
		self.databaseName = 'example.db'

	#QUESTION 1: Pythonic solution to part1 of test
	def time_to_test(self):

		shipdate = pd.read_csv(os.path.join(os.path.join(self.parentPath, self.dataFolder), self.shipmentsPath))
		plans = pd.read_csv(os.path.join(os.path.join(self.parentPath, self.dataFolder), self.plansPath))
		shipdate['received_date'] = shipdate['received_date'].astype('str')
		cells = shipdate.cell_id.unique()
		deltaT = np.zeros(len(cells)-1)

		i = 0
		#for each cell get arrival and first start time
		for cell in cells:
			tempVal = shipdate.loc[shipdate["cell_id"]==cell, "received_date"].iloc[0]

			planTimes = plans.loc[plans["cell_id"]==cell, 'epoch'].sort_values(ascending=True)
			if len(planTimes.index)>0:
				deltaT[i] = int(time.mktime(time.strptime(tempVal, "%m/%d/%Y"))) - planTimes.iloc[0]
				if deltaT[i] < 0:
					deltaT[i] = 0

		#Mean time to test:
		return np.mean(np.nonzero(deltaT))

	#fake connection to db function
	def connect(self):
		#FAKE FUNCTION
		connection = 0

		return connection

	#a special return error function
	def printerr(self, error):
		#fake method to print error to a webpage
		print(error)

	#QUESTION 2: MYSQL should work but function does not. Pycharm ODE not installing SQLlite so I'm using a generic form of this function
	def create_tables(self):

		#connect to db and get cursor
		try:
			con = self.connect(os.path.join(os.path.join(self.BASEPATH, self.databaseName)))
			curs = con.cursor()
		except:
			self.printerr('failed to connect to db')

		# make model database
		try:
			curs.execute("CREATE TABLE model (id, name, cathode, anode, electrolyte, process1, process2)")
		except:
			self.printerr('failed to make model database')

		#make cell database (MySQL, a little rusty with MySQL
		curs.execute("CREATE TABLE cell (cell_id INT, cell_id_alpha VARCHAR(5) NOT NULL, energy DECIMAL(4,4), capacity DECIMAL(4,4), resistance DECIMAL(4,4), OCV DECIMAL(4,4), model_id INT")

		#make test database
		curs.execute("CREATE TABLE tests (test_id INT, test_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, cell_id INT NOT NULL, model_id INT NOT NULL, current DECIMAL(4,4), voltage DECIMAL(4,4))")

	#QUESTION 3A:
	def find_plan(self, input_str, plans):


		plans = pd.Series(data=plans)
		plans = plans.str.find(input_str)
		plans = plans.loc[plans > 0]
		return list(plans)

	#QUESTION 3B:
	def test_find_plan(self):
		listy = pd.read_csv(os.path.join(os.path.join(self.parentPath, self.dataFolder), self.plansPath))


		if len(self.find_plan("AGG", list(listy.iloc[:,0]))) > 0:
			return 1
		else:
			return 0


th = take_home()
print(th.time_to_test())
print(th.test_find_plan())
