#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import donuts_get_pos as getpos
import donuts_get_words as getwords
import random
import socket
import sys
import codecs
import cgitb

class Title:
    def __init__(self):
        self.relWordsObj = getwords.RelatedWords()
        self.posObj = getpos.Title()

    def create(self, words):
        #Get RelWords
        relWords_meishi = self.relWordsObj.get(words, 'meishi')

        #GET Title
        title = self.posObj.create()
        titlePos = title["pos"]
        titleWords = title["words"]

        #置換ポイント選定
        meishiIndex = []
        meishi_x = random.sample([0,2],1)
        doushi_x = -1

        for idx, pos in enumerate(titlePos):
            if pos == '名詞':
                meishiIndex.append( idx )
            elif pos == 'x_meishi':
                meishi_x.append( idx )
            elif pos == 'x_doushi':
                doushi_x = idx

        #置換開始
        for i, idx in enumerate(meishi_x):
            titleWords[idx] = relWords_meishi["ALL"][i]

        if doushi_x > -1:
            relWords_doushi = self.relWordsObj.get(words, 'doushi')
            titleWords[doushi_x] = relWords_doushi["ALL"][0]


        result =  str(' '.join(titleWords)).decode('string-escape')
        return result

if __name__ == '__main__' :
   titleObj = Title()

   for i in range(100):
       print(titleObj.create(["犬","カート・ローゼンウィンケル","像"]))
