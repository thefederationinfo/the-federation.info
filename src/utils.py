#!/usr/env python
# -*- coding: utf-8 -*-
import os
import subprocess

import MySQLdb as mysql

BASEPATH = os.path.dirname(__file__)


class DBConnection(object):
    """Handle DB connectivity."""
    def __init__(self):
        self.read_config()
        self.connect()

    def read_config(self):
        configf = open(BASEPATH + '/config.js', 'rb')
        self.config = {}
        db_config = False
        for line in configf:
            if not db_config:
                if line.find('config.db') > -1:
                    db_config = True
                continue
            if line.find('host') > -1:
                self.config['host'] = line.translate(None, '"\r\n, ').split(':')[1]
            elif line.find('user') > -1:
                self.config['user'] = line.translate(None, '"\r\n, ').split(':')[1]
            elif line.find('password') > -1:
                self.config['password'] = line.translate(None, '"\r\n, ').split(':')[1]
            elif line.find('database') > -1:
                self.config['database'] = line.translate(None, '"\r\n, ').split(':')[1]
                break
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


def call_pod(domain):
    print("Calling pod at domain %s..." % domain)
    subprocess.call(['/usr/bin/wget', 'https://the-federation.info/register/%s' % domain, '-O', '/dev/null'])
