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

    @staticmethod
    def clean_config_line(line):
        remove = ['"', "\n", "\r", ",", " "]
        return line.translate({ord(char):None for char in remove})

    def get_values_from_line(self, line):
        cleaned = self.clean_config_line(line)
        return cleaned.split(":")

    def read_config(self):
        configf = open(BASEPATH + '/config.js', 'r')
        self.config = {}
        db_config = False
        for line in configf:
            if not db_config:
                if line.find('config.db') > -1:
                    db_config = True
                continue
            if (line.find("host") > -1 or line.find("user") > -1 or line.find("password") > -1 or
                    line.find("database") > -1):
                key, value = self.get_values_from_line(line)
                self.config[key] = value
            if {"host", "user", "password", "database"}.issubset(set(self.config.keys())):
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
