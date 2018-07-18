#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import donuts_get_pos as getpos
import donuts_get_words as getwords
import random
import socket
import sys
import codecs
import cgitb
from natto import MeCab
import numpy as np

class Input:
    def __init__(self):
	self.mecab = MeCab()

    def getMeishi(self, text):
	with MeCab('-F%m,%f[0],%h') as nm:
	    """
	    ref : http://develtips.com/python/82
	    """
    	    words = []
	    for n in nm.parse(text, as_nodes=True):
        	node = n.feature.split(',');
        	if len(node) != 3:
            	    continue
        	if node[1] == '名詞':
            	    words.append(node[0])
	return words

class Title:
    def __init__(self):
        self.relWordsObj = getwords.RelatedWords()
        self.posObj = getpos.Title()

    def create(self, words, title_n):
        #Get RelWords
        relWords_meishi = self.relWordsObj.get(words, 'meishi', 10)["ALL"]
	relWords_doushi = self.relWordsObj.get(words, 'doushi', 10)["ALL"]

	titles = {}	
	for n in range(title_n):
	    title, score =  self.merge(relWords_meishi, relWords_doushi)
	    titles[title] = score

	return titles

    def createDonuts(self, words, title_n):
        #Get RelWords
        relWords_meishi = self.relWordsObj.get(words, 'donut', 10)["ALL"]
	words.extend(["お菓子","小麦粉","デザート","食事","おやつ","スイーツ"])
        relWords_doushi = self.relWordsObj.get(words, 'doushi', 10)["ALL"]

        titles = {}
        for n in range(title_n):
            title, score =  self.merge(relWords_meishi, relWords_doushi)
            titles[title] = score

        return titles

    def merge(self, relWords_meishi, relWords_doushi):

	relWords_meishi_keys = list(relWords_meishi.keys())
	relWords_doushi_keys = list(relWords_doushi.keys())
	relWords_score = [] 
	random.shuffle(relWords_meishi_keys)
	random.shuffle(relWords_doushi_keys)

        #GET Title
        title = self.posObj.create()
        titlePos = title["pos"]
        titleWords = title["words"]

        #置換ポイント選定
        #meishiIndex = []
        #meishi_x = random.sample([0,2],1)
 	meishi_x = []
        doushi_x = []

        for idx, pos in enumerate(titlePos):
            if pos == '名詞' or pos == 'x_meishi':
                #meishiIndex.append( idx )
		meishi_x.append( idx )
            #elif pos == 'x_meishi':
            #    meishi_x.append( idx )
            elif pos == '動詞' or pos == 'x_doushi':
                doushi_x.append( idx )

        #置換開始
        for i, idx in enumerate(meishi_x):
            titleWords[idx] = relWords_meishi_keys[i]
	    relWords_score.append(relWords_meishi[relWords_meishi_keys[i]])

        for i, idx in enumerate(doushi_x):
            titleWords[idx] = relWords_doushi_keys[i]
            relWords_score.append(relWords_doushi[relWords_doushi_keys[i]])

        result =  str(' '.join(titleWords)).decode('string-escape')

	cv = self.calcCV(relWords_score)
        return result, int(cv*100)
	
    def calcCV(self, score):
	score = np.array(score)
	cv = np.std(score)/ np.mean(score)
	return cv

if __name__ == '__main__' :
    inputObj = Input()
    inputText = raw_input()
    inputWords = inputObj.getMeishi(inputText)
    titleObj = Title()

    print("START")

    titles = titleObj.create(inputWords, 20)

    #inputWords_proc = ["donut","ドーナッツ"]
    #inputWords_proc.extend(random.sample(inputWords, 2))
    titles_donuts = titleObj.createDonuts(inputWords, 20 )

    for title in titles:
	print(title)

    for title in titles_donuts:
        print(title)
