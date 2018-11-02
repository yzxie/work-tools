#coding=utf-8
import os
from os import system
import time
import sys

#SLOW_QUERY_FILE="./slow-queries.log-20181013"
SLOW_QUERY_FILE="./slow-queries.log-20181025"
def read_slow_query_file_and_analy():
	# [[,,,,],[,,,,]]
	record_lines_set_list = []
	is_next_slow_log = True
	record_lines_set = []

	fd = open(SLOW_QUERY_FILE, 'r')
	while True:
		line = fd.readline()
		if not line:
			break

		#下一条记录的开始		
		if line.startswith("#") and is_next_slow_log == True:
			#把上一条记录存到列表
			if len(record_lines_set) > 0:
				record_lines_set_list.append(record_lines_set)
			#准备接收记录的行
			record_lines_set = []
			is_next_slow_log = False
		
		#一条完整记录包含多行
		record_lines_set.append(line)

		#重置next_slow_log	
		if not line.startswith("#") and is_next_slow_log == False:
			is_next_slow_log = True

	#分析每一条记录
	analy_mysql_slow_log(record_lines_set_list)
	
	fd.close()

def analy_mysql_slow_log(record_lines_set_list):
	total_20_record_count = 0
	total_slow_log_count = 0
	sorted_sql_list = []

	for record_lines_set in record_lines_set_list:
		for i in range(0, len(record_lines_set)):
			record_line = record_lines_set[i]
			if record_line.startswith("# User@Host:") and "172.28.48.20" in record_line:
				total_20_record_count += 1

				# 转换日期并打印记录
				for rl in record_lines_set:
					if rl.startswith("SET timestamp="):
						timestamp = rl[-12:-2]
						time_local = time.localtime(int(timestamp))
						dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

						# 输出22:37
						# if dt.startswith("2018-10-15 22:37"):
						# 	total_slow_log_count += 1
						# 	print "No: %s, Time: %s: Command: %s" % (total_slow_log_count, dt, record_lines_set[0]),
						# 	if record_lines_set[3].startswith("# Query_time:"):
						# 		print record_lines_set[3]
						# 	elif record_lines_set[2].startswith("# Query_time:"):
						# 		print record_lines_set[2]
						# 	# print dt
						# 	# for rl in record_lines_set:
						# 	# 	print rl

						# 输出全部
						total_slow_log_count += 1
						print "No.%s, Time: " % total_slow_log_count, dt
						for i in range(0, len(record_lines_set)):
							if i+1 == len(record_lines_set):
								print record_lines_set[i]
							else:
								print record_lines_set[i],

						# 输出20点
						# if dt.startswith("2018-10-15 20:"):
						# 	total_slow_log_count += 1
						# 	print "No.%s, Time: " % total_slow_log_count, dt
						# 	for i in range(0, len(record_lines_set)):
						# 		if i+1 == len(record_lines_set):
						# 			print record_lines_set[i]
						# 		else:
						# 			print record_lines_set[i],

						# 只输出MySQL语句
						# if record_lines_set[len(record_lines_set)-1].startswith("SELECT"):
						# 	total_slow_log_count += 1
						# 	# 统计数据表时使用：python analy_mysql_slow_log.py | awk -F'FROM' '{print $2}' | awk '{print $1}' | sort | uniq -c
						# 	print "No.%s, Time: %s" % (total_slow_log_count, dt)
						# 	print record_lines_set[len(record_lines_set)-1],

						# 	if record_lines_set[1].startswith("# Query_time:"):
						# 		print record_lines_set[1]
						# 	elif record_lines_set[2].startswith("# Query_time:"):
						# 		print record_lines_set[2]
						# 	#查找耗时
						# 	# query_cost_time = ""
						# 	# for rl2 in record_lines_set:
						# 	# 	if rl2.startswith("# Query_time: "):
						# 	# 		query_cost_time = rl2
						# 	# 		break
						# 	# sorted_sql_list.append(record_lines_set[len(record_lines_set)-1] + query_cost_time)

						# NIO 12号慢日志
						# if record_lines_set[len(record_lines_set)-1].startswith("SELECT") and "for_factor,executed FROM stock_split WHERE  symbol =" in record_lines_set[len(record_lines_set)-1]:
						# 	total_slow_log_count += 1
						# 	# 统计数据表时使用：python analy_mysql_slow_log.py | awk -F'FROM' '{print $2}' | awk '{print $1}' | sort | uniq -c
						# 	print "No.%s, Time: %s" % (total_slow_log_count, dt)
						# 	print record_lines_set[len(record_lines_set)-1],

						# 	if record_lines_set[1].startswith("# Query_time:"):
						# 		print record_lines_set[1]
						# 	elif record_lines_set[2].startswith("# Query_time:"):
						# 		print record_lines_set[2]
						# 	#查找耗时
						# 	# query_cost_time = ""
						# 	# for rl2 in record_lines_set:
						# 	# 	if rl2.startswith("# Query_time: "):
						# 	# 		query_cost_time = rl2
						# 	# 		break

						# 跳出，当前慢查询记录已经处理完
						break
				# 跳出，处理下一个慢查询记录
				break
	#排序和打印SQL语句
	#sorted_unique_sql_list = sorted(list(set(sorted_sql_list)))
	sorted_unique_sql_list = sorted(sorted_sql_list)
	for sql in sorted_unique_sql_list:
		print sql

	print "sorted unique list size: %d" % len(sorted_unique_sql_list)
	print "20 machine match slow record: ", total_slow_log_count

if __name__ == '__main__':
	if len(sys.argv) > 1:
		SLOW_QUERY_FILE="./"+sys.argv[1]
	read_slow_query_file_and_analy()
