#!/usr/env python
# -*- coding: utf-8 -*-
from src.utils import DBConnection

db = DBConnection()

db.cursor.execute("select date, count(1) from stats group by date")

rows = db.cursor.fetchall()
for row in rows:
    db.cursor.execute("update global_stats set pod_count = %s where date = '%s'" % (row["count(1)"], row["date"]))

db.close()
