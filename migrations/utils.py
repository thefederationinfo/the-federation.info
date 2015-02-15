#!/usr/env python
# -*- coding: utf-8 -*-
import os

import MySQLdb as mysql

BASEPATH = os.path.dirname(__file__)


class DBConnection(object):
    """Handle DB connectivity."""
    def __init__(self):
        self.read_config()
        self.connect()

    def read_config(self):
        configf = open(BASEPATH + '/../config.js', 'rb')
        self.config = {}
        for line in configf:
            if line.find('host') > -1:
                self.config['host'] = line.translate(None, '"\r\n, ').split(':')[1]
            elif line.find('user') > -1:
                self.config['user'] = line.translate(None, '"\r\n, ').split(':')[1]
            elif line.find('password') > -1:
                self.config['password'] = line.translate(None, '"\r\n, ').split(':')[1]
            elif line.find('database') > -1:
                self.config['database'] = line.translate(None, '"\r\n, ').split(':')[1]
        configf.close()

    def connect(self):
        self.conn = mysql.connect(
            host=self.config['host'],
            db=self.config['database'],
            user=self.config['user'],
            passwd=self.config['password']
        )
        self.cursor = self.conn.cursor(mysql.cursors.DictCursor)

    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
