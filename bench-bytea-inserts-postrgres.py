import os
import time
import matplotlib.pyplot as plt
import numpy

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
rows=[]
for i in range(0, 1*10**8, 10000000):
    data = psycopg2.Binary(random_stream.read(i))
    start_time = time.time()
    cursor.execute('''insert into bytea_test values (%s)''', (data,))
    duration_random = time.time()-start_time

    data = 'x'*i
    start_time = time.time()
    cursor.execute('''insert into bytea_test values (%s)''', (data,))
    duration_ascii = time.time()-start_time
    kilo_bytes = i / 1000
    row = (kilo_bytes, duration_ascii, duration_random)
    print('{},'.format(row))
    rows.append(row)
m = numpy.array(rows).transpose()
plt.plot(m[0], m[1], label='ascii')
plt.plot(m[0], m[2], label='random')
plt.legend()
plt.xlabel('kilo bytes insert into bytea column')
plt.ylabel('duriation (seconds)')
plt.show()
