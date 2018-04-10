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
	def　__init__(self):
    		"""ローマ字⇔かな変換器を作る"""
    		self.Kana_roman_converter = {
        		'a'  :'ア', 'i'  :'イ', 'u'  :'ウ', 'e'  :'エ', 'o'  :'オ',
        		'ka' :'カ', 'ki' :'キ', 'ku' :'ク', 'ke' :'ケ', 'ko' :'コ',
        		'sa' :'サ', 'shi':'シ', 'su' :'ス', 'se' :'セ', 'so' :'ソ',
        		'ta' :'タ', 'chi':'チ', 'tu' :'ツ', 'te' :'テ', 'to' :'ト',
        		'na' :'ナ', 'ni' :'ニ', 'nu' :'ヌ', 'ne' :'ネ', 'no' :'ノ',
 	       		'ha' :'ハ', 'hi' :'ヒ', 'fu' :'フ', 'he' :'ヘ', 'ho' :'ホ',
        		'ma' :'マ', 'mi' :'ミ', 'mu' :'ム', 'me' :'メ', 'mo' :'モ',
        		'ya' :'ヤ', 'yu' :'ユ', 'yo' :'ヨ',
 		 	'ra' :'ラ', 'ri' :'リ', 'ru' :'ル', 're' :'レ', 'ro' :'ロ',
        		'wa' :'ワ', 'wo' :'ヲ', 'n'  :'ン', 'vu' :'ヴ',
        		'ga' :'ガ', 'gi' :'ギ', 'gu' :'グ', 'ge' :'ゲ', 'go' :'ゴ',
        		'za' :'ザ', 'ji' :'ジ', 'zu' :'ズ', 'ze' :'ゼ', 'zo' :'ゾ',
        		'da' :'ダ', 'di' :'ヂ', 'du' :'ヅ', 'de' :'デ', 'do' :'ド',
        		'ba' :'バ', 'bi' :'ビ', 'bu' :'ブ', 'be' :'ベ', 'bo' :'ボ',
        		'pa' :'パ', 'pi' :'ピ', 'pu' :'プ', 'pe' :'ペ', 'po' :'ポ',
        
                        'a'  :'ァ', 'i' :'ィ', 'u'  :'ゥ', 'e'  :'ェ', 'o'  :'ォ',
			'ya':'ャ', 'yu':'ュ', 'yo':'ョ',
			'v' :'ヴ',
			'ー':'*',
  

        		'kya':'キャ', 'kyi':'キィ', 'kyu':'キュ', 'kye':'キェ', 'kyo':'キョ',
        		'gya':'ギャ', 'gyi':'ギィ', 'gyu':'ギュ', 'gye':'ギェ', 'gyo':'ギョ',
        		'sha':'シャ',               'shu':'シュ', 'she':'シェ', 'sho':'ショ',
        		'ja' :'ジャ',               'ju' :'ジュ', 'je' :'ジェ', 'jo' :'ジョ',
        		'cha':'チャ',               'chu':'チュ', 'che':'チェ', 'cho':'チョ',
        		'dya':'ヂャ', 'dyi':'ヂィ', 'dyu':'ヂュ', 'dhe':'デェ', 'dyo':'ヂョ',
        		'nya':'ニャ', 'nyi':'ニィ', 'nyu':'ニュ', 'nye':'ニェ', 'nyo':'ニョ',
        		'hya':'ヒャ', 'hyi':'ヒィ', 'hyu':'ヒュ', 'hye':'ヒェ', 'hyo':'ヒョ',
        		'bya':'ビャ', 'byi':'ビィ', 'byu':'ビュ', 'bye':'ビェ', 'byo':'ビョ',
        		'pya':'ピャ', 'pyi':'ピィ', 'pyu':'ピュ', 'pye':'ピェ', 'pyo':'ピョ',
        		'mya':'ミャ', 'myi':'ミィ', 'myu':'ミュ', 'mye':'ミェ', 'myo':'ミョ',
        		'rya':'リャ', 'ryi':'リィ', 'ryu':'リュ', 'rye':'リェ', 'ryo':'リョ',
        		'fa' :'ファ', 'fi' :'フィ',               'fe' :'フェ', 'fo' :'フォ',
        		'wi' :'ウィ', 'we' :'ウェ', 
        		'va' :'ヴァ', 'vi' :'ヴィ', 've' :'ヴェ', 'vo' :'ヴォ',
        
        		'kwa':'クァ', 'kwi':'クィ', 'kwu':'クゥ', 'kwe':'クェ', 'kwo':'クォ',
        		'kha':'クァ', 'khi':'クィ', 'khu':'クゥ', 'khe':'クェ', 'kho':'クォ',
        		'gwa':'グァ', 'gwi':'グィ', 'gwu':'グゥ', 'gwe':'グェ', 'gwo':'グォ',
        		'gha':'グァ', 'ghi':'グィ', 'ghu':'グゥ', 'ghe':'グェ', 'gho':'グォ',
        		'swa':'スァ', 'swi':'スィ', 'swu':'スゥ', 'swe':'スェ', 'swo':'スォ',
        		'swa':'スァ', 'swi':'スィ', 'swu':'スゥ', 'swe':'スェ', 'swo':'スォ',
        		'zwa':'ズヮ', 'zwi':'ズィ', 'zwu':'ズゥ', 'zwe':'ズェ', 'zwo':'ズォ',
        		'twa':'トァ', 'twi':'トィ', 'twu':'トゥ', 'twe':'トェ', 'two':'トォ',
        		'dwa':'ドァ', 'dwi':'ドィ', 'dwu':'ドゥ', 'dwe':'ドェ', 'dwo':'ドォ',
        		'mwa':'ムヮ', 'mwi':'ムィ', 'mwu':'ムゥ', 'mwe':'ムェ', 'mwo':'ムォ',
        		'bwa':'ビヮ', 'bwi':'ビィ', 'bwu':'ビゥ', 'bwe':'ビェ', 'bwo':'ビォ',
        		'pwa':'プヮ', 'pwi':'プィ', 'pwu':'プゥ', 'pwe':'プェ', 'pwo':'プォ',
        		'phi':'プィ', 'phu':'プゥ', 'phe':'プェ', 'pho':'フォ',
       			 }
    
    
    		self.Kana_roman_converter_sub = {
        		'si' :'シ'  , 'ti' :'チ'  , 'hu' :'フ' , 'zi':'ジ',
        		'sya':'シャ', 'syu':'シュ', 'syo':'ショ',
        		'tya':'チャ', 'tyu':'チュ', 'tyo':'チョ',
        		'cya':'チャ', 'cyu':'チュ', 'cyo':'チョ',
        		'jya':'ジャ', 'jyu':'ジュ', 'jyo':'ジョ', 'pha':'ファ', 
        		'qa' :'クァ', 'qi' :'クィ', 'qu' :'クゥ', 'qe' :'クェ', 'qo':'クォ',
        
        		'ca' :'カ', 'ci':'シ', 'cu':'ク', 'ce':'セ', 'co':'コ',
        		'la' :'ラ', 'li':'リ', 'lu':'ル', 'le':'レ', 'lo':'ロ',

        		'mb' :'ム', 'py':'パイ', 'tho': 'ソ', 'thy':'ティ', 'oh':'オウ',
       			'by':'ビィ', 'cy':'シィ', 'dy':'ディ', 'fy':'フィ', 'gy':'ジィ',
       			'hy':'シー', 'ly':'リィ', 'ny':'ニィ', 'my':'ミィ', 'ry':'リィ',
        		'ty':'ティ', 'vy':'ヴィ', 'zy':'ジィ',
        
        		'b':'ブ', 'c':'ク', 'd':'ド', 'f':'フ'  , 'g':'グ', 'h':'フ', 'j':'ジ',
        		'k':'ク', 'l':'ル', 'm':'ム', 'p':'プ'  , 'q':'ク', 'r':'ル', 's':'ス',
        		't':'ト', 'v':'ヴ', 'w':'ゥ', 'x':'クス', 'y':'ィ', 'z':'ズ',
        }
        def getYomi(self, s):
                tagger = MeCab.Tagger('-Oyomi')
                #tagger = MeCab.Tagger('mecabrc')
		result = tagger.parse(s)
		print result
                return result

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
	w_i_yomi = mecab.getYomi(w_i)
	w_i_yomi_a = mecab.convStrToA(w_i_yomi)

	results = sql.select(100)
	
	dis_a = {}
	for w_o in results:
		w_o_yomi = mecab.getYomi(w_o)
		w_o_yomi_a = mecab.convStrToA(w_o_yomi)
		dis_a[w_o] = dis.ishiguro_distance(w_i_yomi_a, w_o_yomi_a)  

	for k, v in sorted(dis_a.items(), key=lambda x: x[1] ):
		if v < 0.5:
			print("#############")
			print(k)
			print(v)

