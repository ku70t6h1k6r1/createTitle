# -*- coding: utf-8 -*-
import sqlite3
import random
import numpy as np
import pickle
import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim

class Query:
    def getVec(self, words_list):
        words_list = '","'.join(words_list)
        words_list = '"'+ words_list +'"'
        q = ' SELECT w.word_index, v.x, v.val '
        q += ' FROM wiki_plus_articles_vocab_control w '
        q += ' LEFT OUTER JOIN wiki_plus_articles v '
        q += ' ON w.word_index = v.word_index '
        q += ' WHERE w.word in ({0}) '.format(words_list)
        #q += ' ORDER BY w.word_index, v.x '
        return q

class RelatedWords():
    """
    words_list -> vec_list (at wiki) -> vec_convvert -> related_words_list

    """
    def __init__(self, dbname = 'word2vec.db'):
        self.dbname = dbname
        self.conn = sqlite3.connect(self.dbname)
        self.conn.text_factory = str
        self.c = self.conn.cursor()

        self.qObj = Query()

        with open('meishi_vec.pickle', 'rb') as f:
            self.meishi_vec = pickle.load(f)
        self.vec_size = self.meishi_vec[1]

        #with open('doushi_vec.pickle', 'rb') as f2:
        #    self.doushi_vec = pickle.load(f2)

        #with open('meishi_words.pickle', 'rb') as f3:
        #    self.meshi_words = pickle.load(f3)

        #with open('doushi_words.pickle', 'rb') as f4:
        #    self.doushi_words = pickle.load(f4)

        #restoreTF = RestoreTF()

    def getVec(self, words):
        return None


    def wordsToVec(self, words):
        q = self.qObj.getVec(words)

        vec_dict = {}
        vec = np.full(self.vec_size, 0.0)
        for row in self.c.execute(q):
            if row[0] in vec_dict:
                vec_dict[row[]] = vec

            vec_dict[row[0]][row[1]] = row[2]

        return vec_dict

if __name__ == '__main__' :
    relObj = RelatedWords():
    print(relObj.wordsToVec(["犬","幻"]))
