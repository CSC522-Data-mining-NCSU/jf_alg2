import pdb
import csv
import numpy as np

G = []
with open('all_genre_list','r') as f:
    for genre in f:
        G.append(genre[:-1])

print G

genre = np.zeros(shape=(478,22))

with open('ttt.csv') as f:
    reader = csv.reader(f)
    for i,item in enumerate(reader):
        alpha = item[1].split(',')
        if alpha[0]=='': continue
        for a in alpha:
            j = G.index(a)
            genre[i,j] = 1
#pdb.set_trace()

genre = genre.tolist()
for i,row in enumerate(genre):
    genre[i] = [int(x) for x in row]

with open('test.csv', 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(genre)

pdb.set_trace()
