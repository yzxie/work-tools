#coding=utf-8
import os
from os import system
import pymysql

USERNAME = "root"
PASSWORD = "root"
DBNAME = "hkstock_trade"
HOST = "localhost"
PORT = 3306
FILENAME="./20180228-20181101market-wide.txt"

def parse_market_wide_rows():
	rows = []
	fd = open(FILENAME, 'r')

	while True:
		line = fd.readline()
		if not line:
			break
		columns = line.split('|')
		i = 0
		row = []
		for column in columns:
			column = column.strip()
			if column:
				row.append(column)
		rows.append(row)
	return rows

def bulk_insert_rows_to_market_wide(rows):
	connection = pymysql.connect(
		host=HOST,
		user=USERNAME,
		password=PASSWORD,
		db=DBNAME
	)
	cursor = connection.cursor();
	cursor.execute('SELECT VERSION()')
	data = cursor.fetchone()
	print 'db version %s' % data

	print 'import begin.'
	for row in rows:
		# SQL 插入语句
		sql = """INSERT INTO market_wide(symbol, timestamp, daily_balance, currency, trade_total_value, 
					bid_accumulated_turnover, ask_accumulated_turnover, to_cny_exchange_rate)
        		 VALUES ('%s', '%s', '%d', '%s', '%d', '%d', '%d', '%d')""" \
        		% (row[0], row[1], int(row[2]), row[3], int(row[4]), 
        			int(row[5]), int(row[6]), float(row[7]))
		try:
			cursor.execute(sql)
			connection.commit()
		except Exception as e:
			print 'exception: ', e
			connection.rollback()

	print 'import successfully.'
	connection.close()
	
if __name__ == '__main__':
	rows = parse_market_wide_rows()
	bulk_insert_rows_to_market_wide(rows)