# coding: UTF-8

import sqlite3
import random
import numpy as np

class SqlSet:
    def __init__(self):
        self.dbname = 'word2vec.db'
        self.conn = sqlite3.connect(self.dbname)
        self.conn.text_factory = str
        self.c = self.conn.cursor()

    def select107(self):
        result = []
        for row in self.c.execute('select * from sample_107'):
            result.append(row)
        return result

    def select622(self):
        result = []
        for row in self.c.execute('select * from sample_622'):
            result.append(row)
        return result

    def select_jyoshi_ha(self):
	result = []
        for row in self.c.execute('select word1, word2, word3, word4, word5, word6, word7, pos1, pos2, pos3, pos4, pos5, pos6, pos7 from sample_jyoshi_ha'):
            result.append(row)
        return result

    def close(self):
	       self.conn.close()

class Title:
    def __init__(self):

        self.kigo_a = ['?',' ']
	self.gobi_list = ['んだよね','ってこと']
        self.word_a = []
        self.pos_a = []

        self.title = []
        self.titlePos = []
        self.title2 = []
        self.titlePos2 = []

        self.sql = SqlSet()
        #self.form1_list = self.sql.select622()
        self.form2_list = self.sql.select107()
	self.form1_list = self.sql.select_jyoshi_ha()
        self.sql.close()

    def create(self):
        tmpTitle = random.sample(self.form1_list, 1)

	if tmpTitle[0][7] == '助詞':
	    self.title =  ['x_meishi', tmpTitle[0][0], tmpTitle[0][1], tmpTitle[0][2], tmpTitle[0][3], tmpTitle[0][4], tmpTitle[0][5], tmpTitle[0][6], 'x_meishi']
            self.titlePos =  ['x_meishi', tmpTitle[0][7], tmpTitle[0][8], tmpTitle[0][9], tmpTitle[0][10], tmpTitle[0][11], tmpTitle[0][12], tmpTitle[0][13], 'x_meishi']
        elif tmpTitle[0][7] == '助動詞':
            self.title =  ['x_doushi', tmpTitle[0][1], tmpTitle[0][2], tmpTitle[0][3], tmpTitle[0][4], tmpTitle[0][5], tmpTitle[0][6], 'x_meishi']
            self.titlePos =  ['x_doushi', tmpTitle[0][8], tmpTitle[0][9], tmpTitle[0][10], tmpTitle[0][11], tmpTitle[0][12], tmpTitle[0][13], 'x_meishi']
        elif tmpTitle[0][7] == '記号':
            self.title =  ['x_meishi', tmpTitle[0][1], tmpTitle[0][2], tmpTitle[0][3], tmpTitle[0][4], tmpTitle[0][5], tmpTitle[0][6], 'x_meishi']
            self.titlePos =  ['x_meishi', tmpTitle[0][8], tmpTitle[0][9], tmpTitle[0][10], tmpTitle[0][11], tmpTitle[0][12], tmpTitle[0][13], 'x_meishi']
        else:
            self.title =  [tmpTitle[0][0], tmpTitle[0][1], tmpTitle[0][2], tmpTitle[0][3], tmpTitle[0][4], tmpTitle[0][5], tmpTitle[0][6], 'x_meishi']
            self.titlePos =  [tmpTitle[0][7], tmpTitle[0][8], tmpTitle[0][9], tmpTitle[0][10], tmpTitle[0][11], tmpTitle[0][12], tmpTitle[0][13], 'x_meishi']

	self.title = np.array(self.title)
	self.titlePos = np.array(self.titlePos)
	kigou_index = np.where(self.titlePos == '記号')[0]

	kigou_index = np.r_[kigou_index, np.where(self.titlePos == 'NULL')[0]]
	for idx in kigou_index:
	    self.title[idx] = ' '

	self.title.tolist()
        self.titlePos.tolist()

	"""
	# FOR self.sql.select622()
	if tmpTitle[0][11] == 1064:
            self.title =  [tmpTitle[0][2], tmpTitle[0][3], tmpTitle[0][4], tmpTitle[0][5], '…']
            self.titlePos =  [tmpTitle[0][6], tmpTitle[0][7], tmpTitle[0][8], tmpTitle[0][9], '記号']
        else:
            self.title = [tmpTitle[0][2], tmpTitle[0][3], tmpTitle[0][4],random.sample(self.kigo_a,1)[0]]
            self.titlePos = [tmpTitle[0][6], tmpTitle[0][7], tmpTitle[0][8],'記号']
	"""

        tmpTitle2 = random.sample(self.form2_list, 1)

        if tmpTitle2[0][11] == 537:
	    if tmpTitle2[0][2] in ['なぜ','何故','一体','いったい','果たして','はたして']:
            	self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4], 'x_doushi', 'のか?']
           	self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], 'x_doushi','fix']
	    else :
                self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4], 'x_doushi',random.sample(self.gobi_list,1)[0]]
                self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], 'x_doushi','fix']
        elif tmpTitle2[0][11] == 543:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4],random.sample(self.kigo_a,1)[0] ]
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], '記号']
        elif tmpTitle2[0][11] == 539:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4],  'x_meishi']
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8],  'x_meishi']
        elif tmpTitle2[0][11] == 536:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4], tmpTitle2[0][5], '…']
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], tmpTitle2[0][9], '記号']
        elif tmpTitle2[0][11] == 535:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4], tmpTitle2[0][5]]
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], tmpTitle2[0][9]]
        elif tmpTitle2[0][11] == 542:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4], tmpTitle2[0][5], '…']
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], tmpTitle2[0][9], '記号']
        elif tmpTitle2[0][11] == 534:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4], tmpTitle2[0][5], random.sample(self.kigo_a,1)[0]]
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], tmpTitle2[0][9], '記号']
        elif tmpTitle2[0][11] == 544:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4], tmpTitle2[0][5], '…']
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], tmpTitle2[0][9], '記号']
        elif tmpTitle2[0][11] == 538:
	    if tmpTitle2[0][2] in ['なぜ','何故','いったい','一体','果たして','はたして']:
            	self.title2 = [tmpTitle2[0][2], 'x_meishi', 'なのか?']
            	self.titlePos2 = [tmpTitle2[0][6], 'x_meishi', 'fix']
            else:
                self.title2 = [tmpTitle2[0][2], 'x_meishi', 'なんだよね']
                self.titlePos2 = [tmpTitle2[0][6], 'x_meishi', 'fix']
        else:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4], tmpTitle2[0][5]]
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], tmpTitle2[0][9]]

        title_list = []
        title_list.extend(self.title)
        title_list.extend(['。 '])
        title_list.extend(self.title2)

        title_pos_list = []
        title_pos_list.extend(self.titlePos)
        title_pos_list.extend(['記号'])
        title_pos_list.extend(self.titlePos2)

        return {"words":title_list, "pos":title_pos_list}
