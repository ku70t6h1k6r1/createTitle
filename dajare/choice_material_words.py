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
        wi_a = np.random.randint(0,500000,get_words_n)
        result = []
        for wi in wi_a:
                for row in self.c.execute('select word from wiki_plus_articles_vocab_control where word_index == {0}  and word != ""'.format(wi)):
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
			'ッ':'tu', 
			'ャ':'ya', 'ュ':'yu', 'ョ':'yo',
			'ヴ':'v',
			'ー':'*'
   			} 
   
        def getYomi(self, s):
                tagger = MeCab.Tagger('-Oyomi')
                #tagger = MeCab.Tagger('mecabrc')
		result = tagger.parse(s)
                return result

	def getYomiRoman_with_index(self, s):
		s_kana = self.getYomi(s)
		s_kana_list = list(s_kana.decode('utf-8'))
		s_kana_list = s_kana_list[0:len(s_kana_list) -1 ] #-1　いる？

		s_kana_idx = 0
		s_roman_idx = 0
		s_roman_list = []
		s_roman_initial = self.getYomiRomanList(s)

		for char in s_kana_list:
            		if char.encode('utf-8') in self.Kana_roman_converter.keys():
                                roman = self.Kana_roman_converter[char.encode('utf-8')]
                        else :
                                roman = '*'
			for init in list(roman):
				s_roman_list.append( [s_kana_idx, roman]) 
				s_roman_idx += 1
			s_kana_idx += 1
		return s_kana_list, s_roman_list

	def getYomiRomanList(self, s):
		s_yomi = self.getYomi(s)
		str_roman = ''
		str_list =[]
		s_yomi_list = list(s_yomi.decode('utf-8'))
		s_yomi_list = s_yomi_list[0:len(s_yomi_list) -1 ]
		for char in s_yomi_list:
			if char.encode('utf-8') in self.Kana_roman_converter.keys():
				roman = self.Kana_roman_converter[char.encode('utf-8')]
			else :
				roman = '*'
			str_roman = str_roman + roman 
		for char in str_roman:
			str_list.append(char)
			
		return str_list
	"""
        def convStrToA(self, str):
                str_a = []
                for char in str:
                        str_a.append(char)
                return str_a

	"""

class CreateDajare:
	def __init__(self):
		self.w_l = ''
		self.w_s = ''
		self.mecabObj = Mecab()

	def add(self, w1, w2, s_idx = 0):
		w1_yomi = self.mecabObj.getYomiRoman_with_index(w1)
		w1_kana = w1_yomi[0]
		w1_roman = w1_yomi[1] 
		w2_yomi = self.mecabObj.getYomiRoman_with_index(w2)
		w2_kana = w2_yomi[0]
		w2_roman = w2_yomi[1]

		if(len(w1_roman) > len(w2_roman)):
			w_l_kana = w1_kana
			w_l_roman = w1_roman
			w_s_kana = w2_kana
			w_s_roman = w2_roman
		else:
			w_l_kana = w2_kana
                        w_l_roman = w2_roman
                        w_s_kana = w1_kana
                        w_s_roman = w1_roman

		if s_idx < 0:
			s_kana_idx = w_s_roman[-s_idx ][0]  #重なり始め
			conv_kana_l = len(w_s_kana) -  s_kana_idx 
			dajare =['<']
			dajare.extend(w_s_kana)
			dajare.extend(['>'])
			dajare.extend(w_l_kana[conv_kana_l :len(w_l_kana)])
			

		else:
			s_kana_idx = w_l_roman[s_idx][0]
			dajare = w_l_kana
			dajare[s_kana_idx : s_kana_idx + len(w_s_kana)] = w_s_kana
			dajare.insert(s_kana_idx, '<')
			dajare.insert(s_kana_idx + len(w_s_kana) + 1, '>')		

		dajare_str = ''
		for char in dajare:
			dajare_str = dajare_str + char.encode('utf-8')			

		return dajare_str


if __name__ == '__main__':

	sql = Sql()
	mecab = Mecab()

	#INPUT WORD
	w_i = sys.stdin.readline()
	w_i_yomi_a = mecab.getYomiRomanList(w_i)

	results = sql.select(10000)
	
	dis_a = {}
	for w_o in results:
		w_o_yomi_a = mecab.getYomiRomanList(w_o)
		dis_a[w_o] = dis.ishiguro_distance(w_i_yomi_a, w_o_yomi_a) 

	for k, v in sorted(dis_a.items(), key=lambda x: x[1] ):
		if v[0] < 0.8:
			dajareObj = CreateDajare()
			print("#############")
			print(k)
			print(v[0], v[1])
			print(dajareObj.add(w_i, k, v[1]) )
	"""

	result = mecab.getYomiRoman_with_index(w_i)
	print(result)

	"""
