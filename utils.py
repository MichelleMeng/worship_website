# coding:utf8

from gevent import monkey
monkey.patch_all()
import MySQLdb
import logging
from pool import ConnectionPool
from sql_conn import SqlConn


class SqlPool(SqlConn):

    def __init__(self, host='127.0.0.1', port=3306, user='root', passwd='', db='', charset='utf8', pool_size=2, time_to_sleep=30):
        super(SqlPool, self).__init__(db_name=db)
        self.pool = ConnectionPool(host, port, user, passwd, pool_size=pool_size, time_to_sleep=time_to_sleep)

    def set_auto_trans(self, auto_trans=True):
        self._trans_end = auto_trans

    def get_conn(self, db_name):
        conn = self.pool.get()
        conn.select_db(db_name)
        return conn

    def call_after_commit(self):
        self.auto_close_conn = False
        self.pool.put(self.conn)
        self.conn = None