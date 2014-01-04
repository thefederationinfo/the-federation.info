#!/usr/env python

import MySQLdb as mysql

configf = open('../config.js', 'r')
config = {}
for line in configf:
    if line.find('host') > -1:
        config['host'] = line.translate(None, '"\r\n, ').split(':')[1]
    if line.find('user') > -1:
        config['user'] = line.translate(None, '"\r\n, ').split(':')[1]
    if line.find('password') > -1:
        config['password'] = line.translate(None, '"\r\n, ').split(':')[1]
    if line.find('database') > -1:
        config['database'] = line.translate(None, '"\r\n, ').split(':')[1]
        
conn = mysql.connect(host=config['host'], db=config['database'], user=config['user'], passwd=config['password'])
cursor = conn.cursor(mysql.cursors.DictCursor)

cursor.execute("""SELECT distinct date FROM stats order by date""")
rows = cursor.fetchall()
first = True
for row in rows:
    cursor.execute("""select sum(total_users) as total_users, sum(active_users_halfyear) as active_users_halfyear, sum(active_users_monthly) as active_users_monthly, sum(local_posts) as local_posts from stats where date = %s""", (row['date'],))
    result = cursor.fetchone()
    print result
    first = False

cursor.close()
conn.close()
        


