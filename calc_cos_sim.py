# -*- coding: utf-8 -*-
import sqlite3
import random
import numpy as np
import pickle

def normalize(v, axis=-1, order=2):
    l2 = np.linalg.norm(v, ord = order, axis=axis, keepdims=True)
    l2[l2==0] = 1
    return v/l2

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
    vec_size = wsVec.shape[1]
    print vec_size
    
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

    def get_FromVec(self, wsVec, words_a, vec, outn):
        wiScore = vec * wsVec.T #vecのフォーマットはnumpy.array
	    wiScoreA = np.ravel(wiScore)

        output_w = []
        output_score = []
        
        for i in range(outn):
            output_w.append(self.words_a[np.argsort(wiScoreA)[::-1][i]])
            output_score.append(np.sort(wiScoreA)[::-1][i])

        output = {"words":output_w, "scores":output_score}
	    return output        
    
    def subtract(self, wi1_a, wi2_a, w1_a, w2_a):        
        vec_p = np.zeros(self.vec_size)
        vec_m = np.zeros(self.vec_size)
        
        i = 0
        for wi1 in wi1_a :
            vec_p  = vec_p + w1_a[i] * np.ravel(self.wsVec[self.words_a.index(wi1),:]) 
            i += 1
        
        i = 0
        for wi2 in wi2_a :
            vec_m  = vec_m + w2_a[i] * np.ravel(self.wsVec[self.words_a.index(wi2),:]) 
            i += 1   
       
        vec = vec_p - vec_m
        vec_norm = normalize(vec)
        return vec_norm
     
    def add(self, wi_a, weight_a):
        vec = np.zeros(self.vec_size)
      
        i = 0
        for wi in wi_a :
            vec  = vec + weight_a[i] * np.ravel(self.wsVec[self.words_a.index(wi),:]) 
            i += 1
            
        vec_norm = normalize(vec)
        return vec_norm

    def add_vec(self, wi, vec, weight):
        sum_vec = weight * np.ravel(self.wsVec[self.words_a.index(wi),:]) + vec
        return normalize(sum_vec)
    
    def add_vecvec(self, vec1, vec2):
        sum_vec = vec1 + vec2
        return normalize(sum_vec)
    
    def wi2vec(self, wi):
        return np.ravel(self.wsVec[self.words_a.index(wi),:]) 
    
    def add_noize(self, vec):
        noize = np.diag(np.random.rand(len(vec)))
        vec_w_noize = vec * noize
	return normalize(vec_w_noize)
	
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
    
    def wordsToIndex(self, w_a):
        index = []
        for w in w_a:
            index.append(self.wordToIndex(w))
        return index
        
    def close(self):
	    self.conn.close()
    
    def getWords(self, preWs_a, inputWs_a, pos, n)
        preWs_a = self.WordsToIndex(preWs_a)
        inputWs_a = self.wordsToIndex(inputWs_a)
        inputWsVec_a = add(inputWs_a, np.ones(len(inputWs_a)))
        
	    preW = np.repeat([0.2], len(preWs_a))
        inW = np.ones(len(inputWs_a))
        weight_a = np.r_[preW, inW]
        
    
test = RelatedWords()
wi = RelatedWords.wordToIndex(test, '恋愛')
result = RelatedWords.get(test, wi, 10)
print str(RelatedWords.indexToWords(test, result["words"])).decode('string-escape')

RelatedWords.close(test)

