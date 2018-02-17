# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim
import sqlite3
import random
import pickle

def normalize(v, axis=-1, order=2):
    l2 = np.linalg.norm(v, ord = order, axis=axis, keepdims=True)
    if l2[0]==0:
        l2[0] = 1 
    return v/l2[0]


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

        self.t_vec = []
        self.w_vec = []
        temp_t = {}
        temp_w = {}


        for row in self.c.execute(query):
            temp_t[row[0]] = row[1]
            temp_w[row[0]] = row[2]

        temp_t = sorted(temp_t.items(), key = lambda x: x[0])
        temp_w = sorted(temp_w.items(), key = lambda x: x[0])
        for val in temp_t:
            self.t_vec.append(val[1])

        for val in temp_w:
            self.w_vec.append(val[1])

    def exec_select(self):       
        wi = round(random.uniform(0,108448))
        #wi = 0
        print str(self.indexToWords([wi])).decode('string-escape')
        self.select(wi)
        while  len(self.w_vec) == 0 or len(self.t_vec) == 0 :
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

        output = {"words":self.indexToWords(output_w), "scores":output_score}
	print str(output).decode('string-escape')

    def indexToWords(self, wi_a):
        words = []
        for wi in wi_a:
            result = []
            for row in self.c.execute('select word from articles_vocab_control where word_id == {0}'.format(wi)):
                result.append(row[0])
            words.append(result[0])
        return words

X = tf.placeholder(tf.float32, shape=[None,200])
T = tf.placeholder(tf.float32, shape=[None,200])
Y = tf.nn.sigmoid(T)


#Variableを作成
## INPUT HIDDEN
w_1 = tf.Variable(tf.truncated_normal([200, 400]))
b_1 = tf.Variable(tf.zeros([400]))
z = tf.nn.sigmoid(tf.matmul(X, w_1) + b_1)

## HIDDEN OUTPUT
w_2 = tf.Variable(tf.truncated_normal([400, 200]))
b_2 = tf.Variable(tf.zeros([200]))
output = tf.matmul(z, w_2) + b_2
#output = output / tf.sqrt(tf.reduce_sum(tf.square(output))) 

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
sql.get_FromVec(sql.wsVec, sql.words_a, normalize(np.array(predict_vec[0,])), 40)
#sql.get_FromVec(sql.wsVec, sql.words_a, vec_articles, 20)
#print  np.array(predict_vec[0,])
