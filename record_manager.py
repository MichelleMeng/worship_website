# coding:utf8

import MySQLdb
import datetime
from sql_conn import *
from utils import *

MYSQL_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "port": "3306",
    "passwd": "",
    "charset": "utf8"
}



def get_now_time(format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(format=format)
    

class RecordManager (object):

	TABLE = 'worship'

	def __init__(self, table):
		self.table = table
		self.pool = SqlPool(db="records", **MYSQL_CONFIG)


	def add(self, date, title, record, text, leaflet, create_time=None):
		if not create_time:
			create_time = get_now_time()

		obj_dict = {}
		obj_dict['date'] = date
		obj_dict['title'] = title
		obj_dict['record_link'] = record
		obj_dict['text_link'] = text
		obj_dict['leaflet_link'] = leaflet
		obj_dict['create_time'] = create_time

		last_insert_id = self.pool.insert(self.table, obj_dict=obj_dict)
		obj_dict['id'] = last_insert_id
		return obj_dict

		


if __name__ == '__main__':  #命令行执行的入口
	
	pass
