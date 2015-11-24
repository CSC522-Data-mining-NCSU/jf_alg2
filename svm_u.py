import pdb,csv
import MySQLdb
import MySQLdb.cursors
import math
import random
from sklearn import svm
from sklearn import tree
from collections import OrderedDict
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

def trained_svm(user_id, clf):
    query = 'select movie_genre.*, datediff(date,\'1999-01-01\') as date, grade,rating from ratings,movie_grade,movie_genre where user_id = %d and movie_grade.id=ratings.movie_id and movie_genre.movie_id=ratings.movie_id' % user_id
    cursor.execute(query)
    X = []
    y = []
    for c in cursor:
        genres_info = [int(c['Gay & Lesbian']),
                       int(c['Science Fiction & Fantasy']),
                       int(c['Mystery & Suspense']),
                       int(c['Romance']),
                       int(c['Kids & Family']),
                       int(c['Animation']),
                       int(c['Comedy']),
                       int(c['Faith & Spirituality']),
                       int(c['Horror']),
                       int(c['Adult']),
                       int(c['Western']),
                       int(c['Cult Movies']),
                       int(c['Television']),
                       int(c['Anime & Manga']),
                       int(c['Sports & Fitness']),
                       int(c['Drama']),
                       int(c['Classics']),
                       int(c['Documentary']),
                       int(c['Action & Adventure']),
                       int(c['Art House & International']),
                       int(c['Special Interest']),
                       int(c['Musical & Performing Arts'])]
        date = int(c['date'])
        grade = float(c['grade'])
        rating = float(c['rating'])
        individual = genres_info+[date]+[grade]
        X.append(individual)
        y.append(rating)
    clf.fit(X,y)
    return clf

def test_individual(user_id,movie_id):
    query = 'select movie_genre.*, datediff(date,\'1990-01-01\') as date, grade from movie_grade, movie_genre, ratings where user_id = %d and ratings.movie_id = %d and movie_grade.id=ratings.movie_id and movie_genre.movie_id = ratings.movie_id' % (user_id, movie_id)
    cursor.execute(query)
    for c in cursor:
         genres_info = [int(c['Gay & Lesbian']),
                       int(c['Science Fiction & Fantasy']),
                       int(c['Mystery & Suspense']),
                       int(c['Romance']),
                       int(c['Kids & Family']),
                       int(c['Animation']),
                       int(c['Comedy']),
                       int(c['Faith & Spirituality']),
                       int(c['Horror']),
                       int(c['Adult']),
                       int(c['Western']),
                       int(c['Cult Movies']),
                       int(c['Television']),
                       int(c['Anime & Manga']),
                       int(c['Sports & Fitness']),
                       int(c['Drama']),
                       int(c['Classics']),
                       int(c['Documentary']),
                       int(c['Action & Adventure']),
                       int(c['Art House & International']),
                       int(c['Special Interest']),
                       int(c['Musical & Performing Arts'])]
         date = int(c['date'])
         grade = float(c['grade'])
    return [genres_info+[date]+[grade]]

##############
# evaluation #
##############
def RMSE(predict, actual):
    sum = 0
    n = len(predict)
    for p,a in zip(predict,actual):
        sum += (p - a)**2
    return math.sqrt(sum/n)

ts = open('testResultForm.csv','r')
tsc = csv.reader(ts)
tsc.next()
count = 0
predict = []
actual = []
for line in tsc:
    #if count >= 1000: break
    #if random.random()>0.1:continue
    mid = int(line[0])
    uid = int(line[1])
    a = float(line[2])
    actual.append(a)

    #clf = svm.SVR(kernel='rbf',degree = 2)
    #clf = svm.SVR()
    #clf = tree.DecisionTreeClassifier()
    clf = tree.DecisionTreeRegressor()
    clf = trained_svm(uid, clf)
    r = clf.predict(test_individual(uid,mid))
    r = r.tolist()[0]
    predict.append(r)
    print '%d\t%d\t%f\t%f' % (mid,uid,a,r)
    count += 1

print 'RMSE=',RMSE(predict,actual)

"""
closing the objects
"""
ts.close()
cursor.close()
db.close()

