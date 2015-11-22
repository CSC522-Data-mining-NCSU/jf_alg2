import mysql.connector
import pdb

cnx = mysql.connector.connect(user='root', password = '54321', host = '127.0.0.1', database = 'Netflix')
cursor = cnx.cursor()

query = 'select director from movies'

cursor.execute(query)

director = []

for index, i in enumerate(cursor):
    try:
        p = str(i[0]).split(',')[0]
        director.append(p)
    except:
        print index

cursor.close()
cnx.close()

pdb.set_trace()
