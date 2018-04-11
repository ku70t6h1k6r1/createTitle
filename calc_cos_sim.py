# -*- coding: utf-8 -*-
import sqlite3
import random
import numpy as np
import pickle
import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim


def normalize(v, axis=-1, order=2):
    l2 = np.linalg.norm(v, ord = order, axis=axis, keepdims=True)
    if l2[0]==0:
        l2[0] = 1 
    return v/l2[0]

class RestoreTF:
    def __init__(self):
        #プレースホルダー作成
        self.X = tf.placeholder(tf.float32, shape=[None,200])

        #パラメータ
        self.sess = None

        #Variableを作成
        ## INPUT HIDDEN
        self.w_1 = tf.Variable(tf.truncated_normal([200, 400]))
        self.b_1 = tf.Variable(tf.zeros([400]))
        self.z = tf.nn.sigmoid(tf.matmul(self.X, self.w_1) + self.b_1)

        ## HIDDEN OUTPUT
        self.w_2 = tf.Variable(tf.truncated_normal([400, 200]))
        self.b_2 = tf.Variable(tf.zeros([200]))
        self.output = tf.matmul(self.z, self.w_2) + self.b_2

        #sessionの定義
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())
        self.saver = tf.train.Saver()
        self.saver.restore(self.sess, "./tf_model/model_convert")

    def convert(self, input):
        input_vec = np.array(input).reshape(1,200)
        predict_vec = self.sess.run(self.output, feed_dict={self.X: input_vec})
        return normalize(np.array(predict_vec[0,]))

class RelatedWords:
    dbname = 'word2vec.db'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    c = conn.cursor()

    with open('meishi_vec.pickle', 'rb') as f:
        wsVec = pickle.load(f)    
    vec_size = wsVec.shape[1]
    
    with open('doushi_vec.pickle', 'rb') as f2:
        wsVec2 = pickle.load(f2)

    with open('meishi_words.pickle', 'rb') as f3:
        words_a = pickle.load(f3)

    with open('doushi_words.pickle', 'rb') as f4:
        words2_a = pickle.load(f4)

    restoreTF = RestoreTF()

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
        wiScore = np.matrix(vec[0,:]) * wsVec.T
        wiScoreA = np.ravel(wiScore)

        output_w = []
        output_score = []
        
        for i in range(outn):
            output_w.append(words_a[np.argsort(wiScoreA)[::-1][i]])
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
        for wi in wi_a:
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
<<<<<<< HEAD
        return result[0]

=======
	if len(result) > 0:
            return result[0]
        else:
            query = (''
                ' SELECT vec.x, vec.val '
                ' FROM  wiki_plus_articles vec '
                ' LEFT OUTER JOIN wiki_plus_articles_vocab_control ctr '
                ' ON vec.word_index = ctr.word_index '
                ' WHERE word == \'{0}\' '
                ' ORDER BY vec.x ASC ').format(w)
	        for row in self.c.execute(query):
		        result.append(row[1])

            if len(result) < 1:
                return round(random.uniform(0,10000))
            else:
                fixed_vec = self.restoreTF.convert(result)
                return self.get_FromVec2(self.wsVec, self.words_a, fixed_vec) 
>>>>>>> 7b753813028100375d618a78f764473bc9f259da

    def indexToWords(self, wi_a):
        words = []
        for wi in wi_a:
            result = []
            for row in self.c.execute('select word from articles_vocab_control where word_id == {0}'.format(wi)):
                result.append(row[0])
            words.append(result[0])
        return words
    
    def wordsToIndex(self, w_a):
        index = []
        for w in w_a:
            index.append(self.wordToIndex(w))
        return index
        
    def indexToWord_W(self, wi):
        result = []
        for row in self.c.execute('select word from wiki_plus_articles_vocab_control where word_index == {0}'.format(wi)):
            result.append(row[0])
        return result[0]
        
    def wordToIndex_W(self, w):
        result = []
        #print "wordToindex..."
        for row in self.c.execute('select word_index from wiki_plus_articles_vocab_control where word == \'{0}\''.format(w)):
            result.append(row[0])
        #print "wordToindex...END"
        return result[0]


    def indexToWords_W(self, wi_a):
        words = []
        for wi in wi_a:
            result = []
            for row in self.c.execute('select word from wiki_plus_articles_vocab_control where word_index == {0}'.format(wi)):
                result.append(row[0])
            words.append(result[0])
        return words
    
    def wordsToIndex_W(self, w_a):
        index = []
        for w in w_a:
            index.append(self.wordToIndex_W(w))
        return index
        
    def indexToVec_W(self, wi):
        vec_a = []
        #print "idxToVec..."
        for row in self.c.execute('select val from wiki_plus_articles where word_index == {0} ORDER BY x ASC'.format(wi)):
           vec_a.append(row[0])
        #print "idxToVec...END"
        return np.array(vec_a)

    def get_FromVec2(self, wsVec, words_a, vec):
        wiScore = np.matrix(vec) * wsVec.T
        wiScoreA = np.ravel(wiScore)

        output_w = []
        output_score = []
        
        for i in range(1):
            output_w.append(words_a[np.argsort(wiScoreA)[::-1][i]])
            output_score.append(np.sort(wiScoreA)[::-1][i])

        return self.wordsToIndex(output_w)[0]


    def close(self):
	self.conn.close()

    def open(self):
        dbname = 'word2vec.db'
        conn = sqlite3.connect(dbname)
        conn.text_factory = str
        self.c = conn.cursor()
    
    def getWords(self, preWs_a, inputWs_a, pos, n):
        preWs_a = self.wordsToIndex(preWs_a)
        inputWs_a = self.wordsToIndex(inputWs_a)
        inputWsVec_a = self.add(inputWs_a, np.ones(len(inputWs_a)))

	preW = np.repeat([0.2], len(preWs_a))
        inW = np.ones(len(inputWs_a))
        weight_a = np.r_[preW, inW]

        preWs_a.extend(inputWs_a)
        sumWs = preWs_a
        addVec = self.add(sumWs, weight_a)
        outputVec = self.add_vecvec( addVec, self.add_noize(inputWsVec_a) )
        
        if pos == 'meishi':
            outputWords = self.get_FromVec(self.wsVec, self.words_a, outputVec, 20)
        elif pos =='doushi':
            outputWords = self.get_FromVec(self.wsVec2, self.words2_a, outputVec, 40)
        else:
            print 'sorry!'

        outputWords = outputWords['words']
        return self.indexToWords(random.sample(outputWords, n))
    
    def getUncertenScore(self, w_a):
        wi_a = self.wordsToIndex_W(w_a)
        vec_a = np.zeros(self.vec_size)

        i = 0
        for wi in wi_a:
            if i == 0:
                vec_a = self.indexToVec_W(wi)   
            else:
                vec_a = np.hstack((vec_a, self.indexToVec_W(wi)))
            i += 1

        vec_m = np.reshape(np.array(vec_a), (i,self.vec_size))
        score_m = np.dot(vec_m,vec_m.T) 
        score_a = np.triu(score_m, k = 1).reshape(i * i)
        score_a = np.delete(score_a, np.where(score_a == 0))
        score = abs(np.std(score_a) / np.average(score_a))
        return score

#test = RelatedWords()
#print "VECTRISED !!"
#wi = RelatedWords.wordToIndex(test, 'カート・ローゼンウィンケル')
#result = RelatedWords.get(test, wi, 10)
#print str(RelatedWords.indexToWords(test, result["words"])).decode('string-escape')
#print RelatedWords.getUncertenScore(test, ['犬', 'ペンギン', '時計'])

#print str(RelatedWords.getWords(test, ['犬', 'ペンギン', '時計'], ['恋愛', '女' ], 'meishi', 10)).decode('string-escape')

#RelatedWords.close(test)

