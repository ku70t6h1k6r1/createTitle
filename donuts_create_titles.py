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

	titles = []	
	for n in range(title_n):
	    titles.append(self.merge(relWords_meishi, relWords_doushi))

	return titles

    def createDonuts(self, words, title_n):
        #Get RelWords
        relWords_meishi = self.relWordsObj.get(words, 'donut', 10)["ALL"]
	words.extend(["お菓子","小麦粉","デザート","食事","おやつ","スイーツ"])
        relWords_doushi = self.relWordsObj.get(words, 'doushi', 10)["ALL"]

        titles = []
        for n in range(title_n):
            titles.append(self.merge(relWords_meishi, relWords_doushi))

        return titles

    def merge(self, relWords_meishi, relWords_doushi):	
	random.shuffle(relWords_meishi)
	random.shuffle(relWords_doushi)

        #GET Title
        title = self.posObj.create()
        titlePos = title["pos"]
        titleWords = title["words"]

        #置換ポイント選定
        #meishiIndex = []
        #meishi_x = random.sample([0,2],1)
 	meishi_x = []
        doushi_x = -1

        for idx, pos in enumerate(titlePos):
            if pos == '名詞':
                #meishiIndex.append( idx )
		meishi_x.append( idx )
            elif pos == 'x_meishi':
                meishi_x.append( idx )
            elif pos == 'x_doushi':
                doushi_x = idx

        #置換開始
        for i, idx in enumerate(meishi_x):
            titleWords[idx] = relWords_meishi[i]

        if doushi_x > -1:
            titleWords[doushi_x] = relWords_doushi[0]


        result =  str(' '.join(titleWords)).decode('string-escape')
        return result

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
