# -*- coding: utf-8 -*-
import sqlite3
import random

class SqlSet:
    dbname = 'word2vec.db'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

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

    def close(self):
	self.conn.close()

class Title:
    kigo_a = ['!','?','!?','…']
    word_a = []
    pos_a = []

    title = []
    titlePos = []
    title2 = []
    titlePos2 = []

    sql = SqlSet()
    result_a = SqlSet.select622(sql)
    result2_a = SqlSet.select107(sql)
    SqlSet.close(sql)
	
    def create(self):
        tmpTitle = random.sample(self.result_a, 1)

	if tmpTitle[0][11] == 1064:
           self.title =  [tmpTitle[0][2], tmpTitle[0][3], tmpTitle[0][4], tmpTitle[0][5], '…']
           self.titlePos =  [tmpTitle[0][6], tmpTitle[0][7], tmpTitle[0][8], tmpTitle[0][9], '記号']
        else:
           self.title = [tmpTitle[0][2], tmpTitle[0][3], tmpTitle[0][4],random.sample(self.kigo_a,1)]
           self.titlePos = [tmpTitle[0][6], tmpTitle[0][7], tmpTitle[0][8],'記号']
        return self.title

        tmpTitle2 = random.sample(self.result2_a, 1)

        if tmpTitle[0][11] == 537:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4], 'x_doushi']
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], 'x_doushi']
        elif tmpTitle[0][11] == 543:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4],random.sample(self.kigo_a,1) ]
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], '記号']
        elif tmpTitle[0][11] == 539:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4], tmpTitle2[0][5], 'x_mesihi']
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], tmpTitle2[0][9], 'x_mesihi']
        elif tmpTitle[0][11] == 536:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4], tmpTitle2[0][5], '…']
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], tmpTitle2[0][9], '記号']
        elif tmpTitle[0][11] == 535:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4], tmpTitle2[0][5]]
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], tmpTitle2[0][9]]
        elif tmpTitle[0][11] == 542:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4], tmpTitle2[0][5], '…']
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], tmpTitle2[0][9], '記号']
        elif tmpTitle[0][11] == 534:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4], tmpTitle2[0][5], random.sample(self.kigo_a,1)]
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], tmpTitle2[0][9], '記号']
        elif tmpTitle[0][11] == 544:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4], tmpTitle2[0][5], '…']
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], tmpTitle2[0][9], '記号']
        elif tmpTitle[0][11] == 538:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4], 'x_meishi']
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], 'x_meishi']
        else:
            self.title2 = [tmpTitle2[0][2], tmpTitle2[0][3], tmpTitle2[0][4], tmpTitle2[0][5]]
            self.titlePos2 = [tmpTitle2[0][6], tmpTitle2[0][7], tmpTitle2[0][8], tmpTitle2[0][9]]
    def title(self):
	output = '/'.join(self.title) + '/ /' + '/'.join(self.title2)
	return output

    def titlePos(self):
	output = '/'.join(self.titlePos) + '/ /' + '/'.join(self.titlePos2)
	return output

　　def titlePosA(self):
	return self.titlePos.extend([' ']).extend(self.titlePos2)

   def titleA(self):
	return self.title.extend([' ']).extend(self.title2)
