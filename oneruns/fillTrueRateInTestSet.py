import csv, pdb
import mysql.connector

"""
connecting the database...
"""
cnx = mysql.connector.connect(user='root', password = '54321', host = '127.0.0.1', database = 'Netflix')
cursor = cnx.cursor()

infile = open('../testResults_to_fill.csv','r')
outfile = open('../testResultForm.csv','w')
ins = csv.reader(infile)
ins.next() # ignore the first line
out = csv.writer(outfile)
out.writerow(['movie_id','user_id','actual_rate']) # set up the first line

for row in ins:
    mid = int(row[0])
    uid = int(row[1])
    query = 'select rating from ratings where movie_id = %d and user_id = %d' % (mid,uid)
    cursor.execute(query)
    for x in cursor:
        rate = float(x[0])
    out.writerow([mid,uid,rate])

"""
closing the obejctives
"""
outfile.close()
infile.close()
cursor.close()
cnx.close()
