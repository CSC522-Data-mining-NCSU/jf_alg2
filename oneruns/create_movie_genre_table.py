import csv, pdb
import mysql.connector

###########################
# fetching the genre list #
###########################
genres = []
with open('../all_genre_list','r') as f:
    for g in f:
        genres.append(g[:-1])

N = len(genres)
f = open('../movie_genres.csv','w')
out = csv.writer(f)
title = ['movie_id']+genres
out.writerow(title)

##############################
# connecting to the database #
##############################
cnx = mysql.connector.connect(user='root', password = '54321', host = '127.0.0.1', database = 'Netflix')
cursor = cnx.cursor()
query = 'select id, genre from movies'
cursor.execute(query)

for line in cursor:
    mid = str(line[0])
    gs  = str(line[1]).split(',')
    trow= [0]*N
    try:
        one = [genres.index(i) for i in gs]
        for index in one: trow[index]=1
    except:
        pass
    trow = [mid]+trow
    out.writerow(trow)


cursor.close()
cnx.close()
f.close()
