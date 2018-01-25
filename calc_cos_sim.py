# -*- coding: utf-8 -*-
import sqlite3
import random

#数値ベクトルはnumpy
#言葉は配列
#四則演算系は全てwiかvecでアウトプットはベクトル

class RelatedWords:
    dbname = 'word2vec.db'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    
    def get(self, wi, outn):
        wiScore = 
    end
    
    def get_FromVec(self, wsVec, words_a, vec, outn):
        # main issue
    end
    
    def subtract(self, wi1_a, wi2_a, w1_a, w2_a):
    
        i = 0
        for wi1 in wi1_a:
     
    def add(self, wi_a, weight_a):
        i = 0
           for wi in wi_a:
    
    def add_vec(self, wi, vec, weight):
    
    def add_vecvec(self, vec1, vec2):
    
    def wi2vec(self, wi):
    
    def add_noize(self, vec):
    
    def indexToWord(self, wi):
        
