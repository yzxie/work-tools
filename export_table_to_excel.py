#coding=utf-8
import pymysql
import os
from os import system
import pymysql
import xlwt

USERNAME = "root"
PASSWORD = "root"
DBNAME = "hkstock_trade"
HOST = "localhost"
PORT = 3306
DICT = {
	"N:SHSOUTHBOUNDHK": "港股通（沪）",#connect_sh_hk
    "N:SZSOUTHBOUNDHK": "港股通（深）",#connect_sz_hk
    "N:NORTHBOUNDSH": "沪股通", #connect_hk_sh
    "N:NORTHBOUNDSZ": "深股通" #connect_hk_sz
}

QUOTE_HK_NORTHBOUND_QUOTA = 5.2*pow(10, 10) #"N:NORTHBOUNDSH": "沪股通", "N:NORTHBOUNDSZ": "深股通"
QUOTE_HK_SOUTHBOUND_QUOTA = 4.2*pow(10, 10) #"N:SHSOUTHBOUNDHK": "港股通（沪）", "N:SZSOUTHBOUNDHK": "港股通（深）"

def get_db_cursor():
	conn = pymysql.connect(
		host=HOST,
		user=USERNAME,
		password=PASSWORD,
		db=DBNAME
	)
	return conn.cursor()

def write_excel(filename, rows):
	book = xlwt.Workbook(encoding='utf-8') #不加encoding，会报UnicodeDecodeError: 'ascii' codec can't decode byte 0xe6 in position 0: ordinal not in range(128)
	sheet = book.add_sheet('sheet1')
	# 标题栏
	sheet.write(0, 0, '市场类型')
	sheet.write(0, 1, '日期')
	sheet.write(0, 2, '总额')
	sheet.write(0, 3, '余额')
	sheet.write(0, 4, '净流入额（总额-余额）')

	c = 1
	for row in rows:
		market = ''
		date_str = ''
		total = ''
		quota_balance = ''
		quota_inflow = ''

		for index in range(5):
			if index==0:
				#市场
				market = DICT[row[0]]
				sheet.write(c, index, market)
			elif index==1:
				#日期	
				# row[1]类型为datetime.datetime
				# date_str = row[1].strftime("%Y-%m-%d %H:%M:%S")
				date_str = row[1].strftime("%Y-%m-%d")
				sheet.write(c, index, date_str)
			elif index==2:
				#总额
				if row[0]=='N:NORTHBOUNDSH' or row[0]=='N:NORTHBOUNDSZ':
					total = QUOTE_HK_NORTHBOUND_QUOTA
				elif row[0]=='N:SHSOUTHBOUNDHK' or row[0]=='N:SZSOUTHBOUNDHK':
					total = QUOTE_HK_SOUTHBOUND_QUOTA
				sheet.write(c, index, total)
			elif index==3:
				#余额
				quota_balance = row[2]
				sheet.write(c, index, quota_balance)
			elif index==4:
				#净流入额
				quota_inflow = total - quota_balance
				sheet.write(c, index, quota_inflow)
		c += 1
	book.save(filename)

def export_market_wide():
	cursor = get_db_cursor()
	cursor.execute("select * from market_wide where symbol in ('N:SHSOUTHBOUNDHK', 'N:SZSOUTHBOUNDHK', 'N:NORTHBOUNDSH', 'N:NORTHBOUNDSZ') order by timestamp;")
	
	rows = cursor.fetchall()
	write_excel("净流入额数据.xls", rows)
	cursor.close()

if __name__ == '__main__':
	export_market_wide()