# -*- coding: utf-8 -*-
import sqlite3
import random
import numpy as np
import pickle

#数値ベクトルはnumpy
#言葉は配列
#四則演算系は全てwiかvecでアウトプットはベクトル

class RelatedWords:
    dbname = 'word2vec.db'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    c = conn.cursor()

    with open('meishi_vec.pickle', 'rb') as f:
        wsVec = pickle.load(f)    

    with open('doushi_vec.pickle', 'rb') as f2:
        wsVec2 = pickle.load(f2)

    with open('meishi_words.pickle', 'rb') as f3:
        words_a = pickle.load(f3)

    with open('doushi_words.pickle', 'rb') as f4:
        words2_a = pickle.load(f4)


    def get(self, wi, outn):
        wiScore = self.wsVec[self.words_a.index(wi),:] * self.wsVec.T
	wiScoreA = np.ravel(wiScore)

        output_w = []
        output_score = []

        for i in range(outn):
            output_w.append(self.words_a[np.argsort(wiScoreA)[::-1][i]])
            output_score.append(np.sort(wiScoreA)[::-1][i])

        output = {"words":output_w, "scores":output_score}
	return output


    #def get_FromVec(self, wsVec, words_a, vec, outn):
        # main issue
    
    #def subtract(self, wi1_a, wi2_a, w1_a, w2_a):
    #    i = 0
    #    for wi1 in wi1_a:
     
    #def add(self, wi_a, weight_a):
    #    i = 0
    #       for wi in wi_a:
    
    #def add_vec(self, wi, vec, weight):
    
    #def add_vecvec(self, vec1, vec2):
    
    #def wi2vec(self, wi):
    
    #def add_noize(self, vec):
    def indexToWord(self, wi):
        result = []
        for row in self.c.execute('select word from articles_vocab_control where word_id == {0}'.format(wi)):
            result.append(row[0])
        return result[0]
        
    def wordToIndex(self, w):
        result = []
        for row in self.c.execute('select word_id from articles_vocab_control where word == \'{0}\''.format(w)):
            result.append(row[0])
        return result[0]

    def indexToWords(self, wi_a):
        words = []
        for wi in wi_a:
            result = []
            for row in self.c.execute('select word from articles_vocab_control where word_id == {0}'.format(wi)):
                result.append(row[0])
            words.append(result[0])
        print words
        return words

    def close(self):
	self.conn.close()

test = RelatedWords()
wi = RelatedWords.wordToIndex(test, '恋愛')
result = RelatedWords.get(test, wi, 10)
print str(RelatedWords.indexToWords(test, result["words"])).decode('string-escape')

RelatedWords.close(test)

