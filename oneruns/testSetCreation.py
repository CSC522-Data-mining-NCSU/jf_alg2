import csv,pdb
import mysql.connector
import random

Movie2test = []
for i in range(100):
    m = random.randint(1,14000)
    if m not in Movie2test: Movie2test.append(m)
Movie2test = sorted(Movie2test)

"""
connecting the database...
"""
cnx = mysql.connector.connect(user='root', password = '54321', host = '127.0.0.1', database = 'Netflix')
cursor = cnx.cursor()

outfile = open('../testResults_to_fill.csv','w')
out = csv.writer(outfile)
out.writerow(['movie_id','user_id'])
infile = open('../probe.txt','r')

recording = False
mid = 0
for line in infile:
    if line[-2]==':':
        if int(line[:-2]) in Movie2test:
            mid = int(line[:-2])
            recording = True
        else:
            recording = False
        continue
    if not recording: continue
    uid = int(line[:-1])
    out.writerow([mid, uid])

"""
closing objects
"""
infile.close()
outfile.close()
cursor.close()
cnx.close()
