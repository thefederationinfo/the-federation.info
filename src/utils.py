#!/usr/env python
# -*- coding: utf-8 -*-
import os
import subprocess

import sqlite3

BASEPATH = os.path.dirname(__file__)


class DBConnection(object):
    """Handle DB connectivity."""
    def __init__(self):
        self.connect()

    def connect(self):
        self.conn = sqlite3.connect("thefederation.db")
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()


def call_pod(domain):
    print("Calling pod at domain %s..." % domain)
    subprocess.call(['/usr/bin/wget', 'https://the-federation.info/register/%s' % domain, '-O', '/dev/null'])
