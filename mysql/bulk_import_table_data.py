#coding=utf-8
import os
from os import system

USERNAME = "root"
PASSWORD = "root"
DBNAME = "hkstock_trade"
HOST = "localhost"
PORT = 3306
#DIRNAME = "/Users/xieyizun/Documents/项目文档/db_dump/hkstock_trade/"
DIRNAME= "/Users/xieyizun/work/projects/stock-quote-web/db/"
def list_sql_files_and_import_data():
	for sql_file in os.listdir(r"%s" % DIRNAME):
		print sql_file
		command = """mysql -u %s -p"%s" --host %s --port %s %s < %s""" %(USERNAME, PASSWORD, HOST, PORT, DBNAME, DIRNAME + sql_file)
		system(command)

if __name__ == '__main__':
	list_sql_files_and_import_data()