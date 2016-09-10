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
    

class RecordManager(object):

	TABLE = 'worship'

	TABLE_SCHEMA = '''CREATE TABLE IF NOT EXISTS `worship`(
            `id` int(11) NOT NULL AUTO_INCREMENT,
			`date` date NOT NULL DEFAULT '0000-00-00',
            `title` varchar(64) NOT NULL DEFAULT '',
            `record_link` varchar(64) NOT NULL DEFAULT '',
			`text_link` varchar(64) NOT NULL DEFAULT '',
			`leaflet_link` varchar(64) NOT NULL DEFAULT '',
            `create_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
            `update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
            PRIMARY KEY(`id`)
            ) ENGINE=InnoDB default charset=utf8;'''

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

	def show_all(self):
		ret = self.pool.query(self.table, query_dict={}, fields=['*'])
		for item in ret:
			item['date'] = str(item['date'])
			item['create_time'] = str(item['create_time'])
			item['update_time'] = str(item['update_time'])
		return ret

	def get_by_date(self, date):
		query_dict = {'date': date}
		ret = self.pool.query(self.table, query_dict=query_dict, fields=['*'])
		for item in ret:
			item['date'] = str(item['date'])
			item['create_time'] = str(item['create_time'])
			item['update_time'] = str(item['update_time'])
		if not ret:
			return []
		return ret

	def get_by_id(self, entry_id):
		query_dict = {'id': entry_id}
		ret = self.pool.query(self.table, query_dict=query_dict, fields=['*'])
		for item in ret:
			item['date'] = str(item['date'])
			item['create_time'] = str(item['create_time'])
			item['update_time'] = str(item['update_time'])
		if not ret:
			return []
		return ret


if __name__ == '__main__':  #命令行执行的入口
	# r_manager = RecordManager(RecordManager.TABLE)
	# r_manager.add(20160904, 'title_loooooooooooooooong', 'record2', 'text2', 'leaf2')
	# print r_manager.show_all()
	pass
