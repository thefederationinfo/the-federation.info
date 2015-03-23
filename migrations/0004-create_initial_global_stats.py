#!/usr/env python

import MySQLdb as mysql
from datetime import timedelta

configf = open('config.js', 'r')
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
configf.close()        

conn = mysql.connect(host=config['host'], db=config['database'], user=config['user'], passwd=config['password'])
cursor = conn.cursor(mysql.cursors.DictCursor)

cursor.execute("""SELECT distinct date FROM stats order by date""")
rows = cursor.fetchall()
for row in rows:
    cursor.execute("""select sum(total_users) as total_users, sum(active_users_halfyear) as active_users_halfyear, sum(active_users_monthly) as active_users_monthly, sum(local_posts) as local_posts from stats where date = %s""", (row['date'],))
    result = cursor.fetchone()
    print result
    prevday = row['date']-timedelta(days=1)
    cursor.execute("""select sum(total_users) as total_users, sum(active_users_halfyear) as active_users_halfyear, sum(active_users_monthly) as active_users_monthly, sum(local_posts) as local_posts from stats where date = %s""", (prevday,))
    prevresult = cursor.fetchone()
    if prevresult and prevresult['total_users']:
        result['new_users'] = result['total_users'] - prevresult['total_users']
    else:
        result['new_users'] = 0
    if prevresult and prevresult['local_posts']:
        result['new_posts'] = result['local_posts'] - prevresult['local_posts']
    else:
        result['new_posts'] = 0
    cursor.execute("""insert into global_stats (date, total_users, active_users_halfyear, active_users_monthly, local_posts, new_users, new_posts) values (%s, %s, %s, %s, %s, %s, %s)""", (row['date'], result['total_users'], result['active_users_halfyear'], result['active_users_monthly'], result['local_posts'], result['new_users'], result['new_posts'],))

conn.commit()
cursor.close()
conn.close()
        


