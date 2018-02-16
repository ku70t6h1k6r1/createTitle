# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim
import sqlite3
import random

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
        self.select(wi)
        while  len(self.w_vec) == 0 or len(self.t_vec) == 0:
            print "Nan!"
            wi = round(random.uniform(0,108448))
            self.select(wi)


#reference
#https://localab.jp/blog/simple-neural-network-using-tensorflow/
#http://airoboticsandsoon.hatenablog.jp/entry/2017/10/28/212245
#http://nnadl-ja.github.io/nnadl_site_ja/chap3.html

class NNW:
    def __init__(self):

        #プレースホルダー作成
        self.X = tf.placeholder(tf.float32, shape=[None,200])
        self.T = tf.placeholder(tf.float32, shape=[None,200])
        #self.Y = tf.nn.sigmoid(self.T)
        self.Y = self.T        

        #パラメータ
        self.acc = []
        self.sum_out = None
        self.sum_Y = None
        self.sess = None
        self.train_sep = None
        self.accuracy = None

        #Variableを作成
        ## INPUT HIDDEN
        self.w_1 = tf.Variable(tf.truncated_normal([200, 50]))
        self.b_1 = tf.Variable(tf.zeros([50]))
        self.z = tf.nn.sigmoid(tf.matmul(self.X, self.w_1) + self.b_1)

        ## HIDDEN OUTPUT
        self.w_2 = tf.Variable(tf.truncated_normal([50, 200]))
        self.b_2 = tf.Variable(tf.zeros([200]))
        #self.output = tf.nn.sigmoid(tf.matmul(self.z, self.w_2) + self.b_2)
        self.output = tf.matmul(self.z, self.w_2) + self.b_2
        self.output = self.output / tf.sqrt(tf.reduce_sum(tf.square(self.output)))

        #誤差関数は交差エントロピーを使用
        self.cross_entropy = -tf.reduce_sum(self.Y * tf.log(self.output) + (1 - self.Y) * tf.log(1 - self.output))

        #勾配降下法(gradient descent)を使用して最適化(optimization)
        #学習率0.1で交差エントロピーの最小化を行う
        self.train_step = tf.train.GradientDescentOptimizer(0.1).minimize(self.cross_entropy)
        self.accuracy = 1 - tf.reduce_sum(tf.abs(self.Y - self.output)) / 200 #len(Y)
        self.sum_out = self.output
        self.sum_Y = tf.reduce_sum(self.Y)

        #sessionの定義
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

    def learn(self, input, output):
        #学習を行う
        self.sess.run(self.train_step, feed_dict={self.X:input, self.T:output})
        #acc_val = self.accuracy.eval(session=self.sess, feed_dict={self.X:input, self.T:output})
        #print ('正答率:{0}'.format(acc_val))
        #print self.sum_out.eval(session=self.sess, feed_dict={self.X:input, self.T:output})
        #print self.sum_Y.eval(session=self.sess, feed_dict={self.X:input, self.T:output})
        #self.acc.append(acc_val)

#TEST
nnw = NNW()
sql = SqlSet()

for i in range(500000):
    sql.exec_select()
    vec_wiki = np.array(sql.w_vec).reshape(1,200)
    vec_articles = np.array(sql.t_vec).reshape(1,200)
    #print vec_wiki
    #print vec_articles
    nnw.learn(vec_wiki, vec_articles)
    print i

saver = tf.train.Saver()
saver.save(nnw.sess, './tf_model/model_convert')
