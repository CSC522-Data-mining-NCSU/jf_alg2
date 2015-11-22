import pdb,csv
import MySQLdb
import MySQLdb.cursors
import math
from sklearn import svm
from WeightFinder import *

wf = WeightFinder()
#########################################################################
# fetching the test sets                                                #
# WARNING: ignore the last movie in the test set (just for convenience) #
#########################################################################
movies = []
users = []
actual_rates=[]
with open('testResultForm.csv','r') as f:
    ts = csv.reader(f)
    ts.next() # ignore the first line
    tmp_u = []
    tmp_r = []
    for td in ts:
        mid = int(td[0])
        if mid not in movies:
            movies.append(mid)
            users.append(tmp_u)
            tmp_u = []
            actual_rates.append(tmp_r)
            tmp_r = []
        uid = int(td[1])
        ar  = float(td[2])
        tmp_u.append(uid)
        tmp_r.append(ar)
del movies[-1]
users.pop(0)
actual_rates.pop(0)
print 'Fetching test set---DONE!'

###########################
# accessing  the database #
###########################
db = MySQLdb.Connection(host='127.0.0.1',user='root',passwd='54321',db='Netflix')
cursor = db.cursor(MySQLdb.cursors.DictCursor)

def train_data(movie_id):
    query = 'select weight as reputation, rating from ratings,user_info where movie_id = %d and user_info.id = ratings.user_id' % movie_id
    cursor.execute(query)
    rows = cursor.fetchall()
    reputation = [float(row['reputation']) for row in rows]
    rating     = [float(row['rating']) for row in rows]
    return reputation, rating

#############
# evulation #
#############
def RMSE(predict, actual):
    sum = 0
    n = len(predict)
    for p,a in zip(predict,actual):
        sum += (p - a)**2
    return math.sqrt(sum/n)

###############
for m_i, m in enumerate(movies):
    rep, rat = train_data(m)
    X = [[i] for i in rep]
    y = rat
    if m_i < 65 or len(y) > 10000: continue
    clf = svm.SVR()
    clf.fit(X,y)
    XX = [[wf.get_user_weight(i)] for i in users[m_i]]
    e = clf.predict(XX)
    e = e.tolist()
    print m, len(e), RMSE(e, actual_rates[m_i])


"""
closing the objects
"""
cursor.close()
db.close()

