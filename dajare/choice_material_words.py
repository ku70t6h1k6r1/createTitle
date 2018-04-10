# -*- coding: utf-8 -*-
import sqlite3
import random
import sys
import numpy as np
import MeCab
import distance as dis

class Sql:
    dbname = '../word2vec.db'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    c = conn.cursor()

    def select(self, get_words_n):
        wi_a = np.random.randint(0,100000,get_words_n)
        result = []
        for wi in wi_a:
                for row in self.c.execute('select word from wiki_plus_articles_vocab_control where word_index == {0}'.format(wi)):
                        result.append(row[0])

        return result

class Mecab:
	def __init__(self):
    		"""ローマ字⇔かな変換器を作る"""
    		self.Kana_roman_converter = {
        		'ア':'a'  , 'イ':'i'  , 'ウ':'u'  , 'エ':'e'  , 'オ':'o'  ,
        		'カ':'ka' , 'キ':'ki' , 'ク':'ku' , 'ケ':'ke' , 'コ':'ko' ,
        		'サ':'sa' , 'シ':'shi', 'ス':'su' , 'セ':'se' , 'ソ':'so' ,
        		'タ':'ta' , 'チ':'chi', 'ツ':'tu' , 'テ':'te' , 'ト':'to' ,
        		'ナ':'na' , 'ニ':'ni' , 'ヌ':'nu' , 'ネ':'ne' , 'ノ':'no' ,
 	       		'ハ':'ha' , 'ヒ':'hi' , 'フ':'fu' , 'ヘ':'he' , 'ホ':'ho' ,
        		'マ':'ma' , 'ミ':'mi' , 'ム':'mu' , 'メ':'me' , 'モ':'mo' ,
        		'ヤ':'ya' , 'ユ':'yu' , 'ヨ':'yo' ,
 		 	'ラ':'ra' , 'リ':'ri' , 'ル':'ru' , 'レ':'re' , 'ロ':'ro' ,
        		'ワ':'wa' , 'ヲ':'wo' , 'ン':'n'  ,
        		'ガ':'ga' , 'ギ':'gi' , 'グ':'gu' , 'ゲ':'ge' , 'ゴ':'go' ,
        		'ザ':'za' , 'ジ':'ji' , 'ズ':'zu' , 'ゼ':'ze' , 'ゾ':'zo' ,
        		'ダ':'da' , 'ヂ':'ji' , 'ヅ':'zu' , 'デ':'de' , 'ド':'do' ,
        		'バ':'ba' , 'ビ':'bi' , 'ブ':'bu' , 'ベ':'be' , 'ボ':'bo' ,
        		'パ':'pa' , 'ピ':'pi' , 'プ':'pu' , 'ペ':'pe' , 'ポ':'po' ,
        
                        'ァ':'a', 'ィ':'i', 'ゥ':'u', 'ェ':'e', 'ォ':'o',
			'ャ':'ya', 'ュ':'yu', 'ョ':'yo',
			'ヴ':'v',
			'ー':'*'
   			} 
   
        def getYomi(self, s):
                tagger = MeCab.Tagger('-Oyomi')
                #tagger = MeCab.Tagger('mecabrc')
		result = tagger.parse(s)
		print result
                return result

	def getYomiRoman(self, s):
		s_yomi = self.getYomi(s)
		str_list = []
		s_yomi_list = list(s_yomi.decode('utf-8'))
		s_yomi_list = s_yomi_list[0:len(s_yomi_list) -1 ]
		print(s_yomi_list)
		for char in s_yomi_list:
			key = [k for k, v in self.Kana_roman_converter.items() if char.encode('utf-8') in v]
			str_list.append(key)
			print(char)
			print("key is ",key)
		return np.array(str_list)

        def convStrToA(self, str):
                str_a = []
                for char in str:
                        str_a.append(char)
                return str_a


if __name__ == '__main__':
	sql = Sql()
	mecab = Mecab()

	#INPUT WORD
	w_i = sys.stdin.readline()
	w_i_yomi_a = mecab.getYomiRoman(w_i)

	results = sql.select(100)
	
	dis_a = {}
	for w_o in results:
		w_o_yomi_a = mecab.getYomiRoman(w_o)
		dis_a[w_o] = dis.ishiguro_distance(w_i_yomi_a, w_o_yomi_a)  

	for k, v in sorted(dis_a.items(), key=lambda x: x[1] ):
		if v < 0.5:
			print("#############")
			print(k)
			print(v)

