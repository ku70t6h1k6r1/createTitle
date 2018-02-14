# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim
import sqlite3
import random
import pickle

class SqlSet:
    dbname = 'word2vec.db'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    c = conn.cursor()
    index = []
    t_vec = []    
    w_vec = []

    with open('meishi_vec.pickle', 'rb') as f:
        wsVec = pickle.load(f)    
    vec_size = wsVec.shape[1]
    
    with open('doushi_vec.pickle', 'rb') as f2:
        wsVec2 = pickle.load(f2)

    with open('meishi_words.pickle', 'rb') as f3:
        words_a = pickle.load(f3)

    with open('doushi_words.pickle', 'rb') as f4:
        words2_a = pickle.load(f4)

    def select(self, wi):
        query = (''
                'SELECT '
                'x as node_n '
                ',val_a as Y '
                ',val_w as X '
                ' FROM convert '
                ' WHERE word_index_a = {0} '
                ' ORDER BY x ASC'
                '').format(wi)
        self.index = []
        self.t_vec = []
        self.w_vec = []
        for row in self.c.execute(query):
            print row
            self.index.append(row[0])
            self.t_vec.append(row[1])
            self.w_vec.append(row[2])

    def exec_select(self):       
        wi = round(random.uniform(0,108448))
        self.select(wi)
        while  len(self.w_vec) == 0 or len(self.t_vec) == 0 or len(self.index) == 0  :
            print "Nan!"
            wi = round(random.uniform(0,108448))
            self.select(wi)

    def get_FromVec(self, wsVec, words_a, vec, outn):
        wiScore = np.matrix(vec) * wsVec.T
        wiScoreA = np.ravel(wiScore)

        output_w = []
        output_score = []
        
        for i in range(outn):
            output_w.append(words_a[np.argsort(wiScoreA)[::-1][i]])
            output_score.append(np.sort(wiScoreA)[::-1][i])

        output = {"words":output_w, "scores":output_score}
	print output

X = tf.placeholder(tf.float32, shape=[None,200])
T = tf.placeholder(tf.float32, shape=[None,200])
Y = tf.nn.sigmoid(T)


#Variableを作成
## INPUT HIDDEN
w_1 = tf.Variable(tf.truncated_normal([200, 50]))
b_1 = tf.Variable(tf.zeros([50]))
z = tf.nn.sigmoid(tf.matmul(X, w_1) + b_1)

## HIDDEN OUTPUT
w_2 = tf.Variable(tf.truncated_normal([50, 200]))
b_2 = tf.Variable(tf.zeros([200]))
output = tf.matmul(z, w_2) + b_2


sess=tf.Session()
saver = tf.train.Saver()
saver.restore(sess, "./tf_model/model_convert")

sql = SqlSet()
sql.exec_select()
vec_wiki = np.array(sql.w_vec).reshape(1,200)
vec_articles = np.array(sql.t_vec).reshape(1,200)

predict_vec = sess.run(output, feed_dict={X: vec_wiki})
#print predict_vec[0,].tolist()
#print sql.index
#print vec_articles
print "########"
sql.get_FromVec(sql.wsVec, sql.words_a, list(predict_vec[0,]), 20)
sql.get_FromVec(sql.wsVec, sql.words_a, vec_articles, 20)

