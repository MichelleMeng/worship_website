# coding: utf-8

from gevent import monkey
monkey.patch_all()
import gevent
from gevent.queue import Queue, Empty

import logging
import datetime
import MySQLdb

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("sqlpool")


def _singleton(cls, *args, **kwargs):
    _pool = {}
    def _wrap(*args2, **kwargs2):
        host = kwargs2.get('host', '')
        port = kwargs2.get('port', '')
        key = '%s:%s' % (host, port)
        if key not in _pool:
            _pool[key] = cls(*args2, **kwargs2)
        return _pool[key]
    return _wrap


@_singleton
class ConnectionPool:

    def __init__(self, host='', port=3306, user='', passwd='', pool_size=10, time_to_sleep=30):
        self.username = user
        self.password = passwd
        self.host = host
        self.port = int(port)

        self.max_pool_size = pool_size
        self.pool = None
        self.time_to_sleep = time_to_sleep
        self._initialize_pool()

    def get_conn(self):
        conn = MySQLdb.connect(host=self.host, user=self.username,
                          passwd=self.password, port=self.port, charset="utf8")
        return conn

    def get(self):
        try:
            return self.pool.get(timeout=0.1)
        except Empty:
            return self.get_conn()

    def put(self, conn):

        if self.pool.qsize() >= self.max_pool_size:
            LOGGER.debug("pool size is full, will not push")
            self._close_conn(conn)
        else:
            self.pool.put_nowait(conn)

    @staticmethod
    def _close_conn(conn):
        try:
            conn.close()
        except MySQLdb.OperationalError as e:
            LOGGER.error("conn close fail: %s" % str(e))

    def get_pool_size(self):
        return self.pool.qsize()

    def get_initialized_connection_pool(self):
        return self.pool

    def supply_conn_for_pool(self):
        current_pool_size = self.pool.qsize()
        if current_pool_size < self.max_pool_size:
            for _ in range(0, self.max_pool_size - current_pool_size):
                try:
                    conn = self.get_conn()
                    self.pool.put_nowait(conn)
                except MySQLdb.OperationalError as e:
                    LOGGER.error("Cannot initialize connection pool - retrying in {} seconds".format(self.time_to_sleep))
                    LOGGER.exception(e)
                    break

    def _initialize_pool(self):
        self.pool = Queue()
        self.supply_conn_for_pool()
        gevent.spawn(self._check_for_connection_loss)

    def _check_for_connection_loss(self):
        while True:

            try:
                conn = self.pool.get_nowait()
            except Empty:
                conn = None

            if not self._ping(conn):
                LOGGER.debug("conn {} is loss".format(conn))
            else:
                LOGGER.debug("conn {} is alive".format(conn))
                self.pool.put_nowait(conn)

            if self.pool.qsize() < self.max_pool_size / 2:
                self.supply_conn_for_pool()

            LOGGER.debug("pool size is {}, check at {}".format(self.pool.qsize(), datetime.datetime.now()))
            gevent.sleep(self.time_to_sleep)

    def _ping(self, conn):
        if conn is None:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute('select 1;')
            return True

        except MySQLdb.OperationalError as e:
            LOGGER.warn('Cannot connect to mysql - retrying in {} seconds'.format(self.time_to_sleep))
            LOGGER.exception(e)
            return False