import os
import time

import psycopg2

db = psycopg2.connect(dbname=os.environ['USER'])
cursor = db.cursor()
cursor.execute('''
drop table if exists bytea_test;
create table bytea_test (
    data bytea
    )
;
''')
random_stream = open('/dev/urandom', 'rb')
for i in range(0, 1*10**9, 100000):
    start_time = time.time()
    data = psycopg2.Binary(random_stream.read(i))
    cursor.execute('''insert into bytea_test values (%s)''', (data,))
    duration_random = time.time()-start_time

    start_time = time.time()
    data = 'x'*i
    cursor.execute('''insert into bytea_test values (%s)''', (data,))
    duration_ascii = time.time()-start_time

    print('{};{};{}'.format(i, duration_ascii, duration_random))
