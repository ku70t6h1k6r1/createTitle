# -*- coding: utf-8 -*-
import sqlite3
import random
import numpy as np
import pickle
import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim


# FUNCTIONS
def normalize(v, axis=-1, order=2):
    l2 = np.linalg.norm(v, ord = order, axis=axis, keepdims=True)
    if l2[0]==0:
        l2[0] = 1 
    return v/l2[0]

class Query:
    def getVec(self, words_list):
        words_list = '","'.join(words_list)
        words_list = '"'+ words_list +'"'
        q = ' SELECT w.word, v.x, v.val '
        q += ' FROM wiki_plus_articles_vocab_control w '
        q += ' LEFT OUTER JOIN wiki_plus_articles v '
        q += ' ON w.word_index = v.word_index '
        q += ' WHERE w.word in ({0}) '.format(words_list)
        #q += ' ORDER BY w.word_index, v.x '
        return q

    def getWord(self, index):
        q = 'SELECT word FROM articles_vocab_control WHERE word_id = {0}'.format(index)
	return q

    def getMisterDonutsMenu(self):
	q = 'SELECT menu_name FROM mister_donuts_menu '
        return q

# CLASSES

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
    """
    words_list -> vec_list (at wiki) -> vec_convvert -> related_words_list

    """
    def __init__(self, dbname = 'word2vec.db', vecSize = 200):
        self.vec_size = vecSize

	self.dbname = dbname
        self.conn = sqlite3.connect(self.dbname)
        self.conn.text_factory = str
        self.c = self.conn.cursor()

        self.qObj = Query()

        with open('meishi_vec.pickle', 'rb') as f:
            self.meishi_vec = pickle.load(f)
        
        with open('doushi_vec.pickle', 'rb') as f2:
            self.doushi_vec = pickle.load(f2)

        with open('meishi_words.pickle', 'rb') as f3:
            self.meshi_words = pickle.load(f3)

        with open('doushi_words.pickle', 'rb') as f4:
            self.doushi_words = pickle.load(f4)

        self.restoreTF = RestoreTF()

	#menuのときは↓
        #q = self.qObj.getMisterDonutsMenu()
	#self.donuts = []
        #for row in self.c.execute(q):
	#    self.donuts.append(row[0])
     	
	self.donuts = ['ドーナツ', 
			'牛乳',
			'バター',
			'穴',
			'輪型',
			'はらドーナッツ', 
			'フロレスタ',
			'ミスタードーナツ',
			'ダンキンドーナツ',
			'小麦粉',
			'砂糖',
			'卵',
			'160℃の油',
			'円',
			'ベーキングパウダー',
			'ポン・デ・リング',
			'オールドファッション',
			'ダスキン'
			]


    def get(self, words, pos = "meishi", return_n = 10):
	
	if pos == "meishi":
	    vecs = self.wordsToVecProc(words)
	    words = self.vecsToRelatedWords(self.meshi_words, self.meishi_vec, vecs, return_n)
	elif pos == "doushi":
	    vecs = self.wordsToVecProc(words)
	    words = self.vecsToRelatedWords(self.doushi_words, self.doushi_vec, vecs, return_n)
	elif pos == "donut":
	     words.extend(self.donuts)
	     words = random.sample(words, len(self.donuts)) if len(self.donuts) < len(words) else random.sample(words, len(words))
	     words_dict ={} 
	     
             for i, word in enumerate(words):
		words_dict[word] = random.random() 		
		#if i > len(self.donuts):
		#    break

	     words = {}
	     words["ALL"] = words_dict
	     #words = {"ALL":random.sample(words, return_n)} if len(words) > return_n else {"ALL":random.sample(words, len(words))}

	#words_list = {} #words_list["words"] = ["related_words_1", "related_words_2", ....]
	#for key in words :
	#    related_words_list = []
	
	#    for relWords in words[key]:
	#	related_words_list.append(relWords)

	#    random.shuffle(related_words_list)
	#    words_list[key] = related_words_list

	return words

    def vecsToRelatedWords(self, corpus_words, corpus_vec, vecs, n_out):

        output = {}
	for key in vecs:	    
	    vec = vecs[key]

            scores = np.matrix(vec) * corpus_vec.T
            scores = np.ravel(scores)

            related_words = {}
        
            for i in range(n_out):
		index_rel = corpus_words[np.argsort(scores)[::-1][i]]
		q = self.qObj.getWord(index_rel)
		for row in self.c.execute(q):
		    key_rel_str = row[0]
		related_words[key_rel_str] = np.sort(scores)[::-1][i]

            output[key] = related_words
	return output    

    def wordsToVec(self, words):
	"""
	GOT FROM WIKIPEDIA CORPUS
	"""
        q = self.qObj.getVec(words)
        vec_dict = {}
        
        for row in self.c.execute(q):
            if not row[0] in vec_dict:
                vec_dict[row[0]] = np.full(self.vec_size, 0.0)

            vec_dict[row[0]][row[1]] = row[2]

        return vec_dict

    def wordsToVecProc(self, words):
	"""
	PREFERED TOSHI-DENSETSU CORPUS
	"""
	vec_dict = self.wordsToVec(words)
	vec_dict_proc = {}

	merge_vec = np.full(self.vec_size, 0.0)
	for key in vec_dict:
	    vec_dict_proc[key] = self.restoreTF.convert(vec_dict[key])
	    merge_vec = merge_vec + vec_dict[key]	 

	vec_dict_proc["ALL"] = self.restoreTF.convert(normalize(merge_vec))
	return vec_dict_proc


if __name__ == '__main__' :
    relObj = RelatedWords()
    relatedWords = relObj.get(["犬","城","カート・ローゼンウィンケル"], "donut")
    print(relatedWords)
    for key_i in relatedWords:
	print("=====")
	print(key_i)
	for key_rel in relatedWords[key_i]:
	     print(key_rel)
	     print(relatedWords[key_i][key_rel])
