#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import create_title_pos_E as getpos
import donuts_get_words as getwords
import random
import socket
import sys
import codecs
import cgitb

class Title:
    def __init__(self):
        self.relWordsObj = getWords.RelatedWords()
        self.posObj = getpos.Title()

    def create(self, words):
        #Get RelWords
        relWords_meishi = self.relWordsObj.get(words, 'meishi')

        #Titleをmergeように成型
        self.posObj.create()
        titlePos = self.posObj.titlePosA()
        titleWords = self.posObj.titleA()

        meishiIndex = []
        #meishiWords = []
        defaultIndex = [0,2]

        meishi_x = random.sample(defaultIndex,1)
        doushi_x = -1

        for idx, pos in enumerate(titlePos):
            if pos == '名詞':
                meishiIndex.append( idx )
            elif pos == 'x_meishi':
                meishi_x.append( idx )
            elif pos == 'x_doushi':
                doushi_x = i

        #for idx in meishiIndex:
        #    meishiWords.append(titleWords[idx])


        #置換開始
        for i, idx in enumerate(meishi_x):
            titleWords[idx] = relwords_meishi["ALL"][i]


        if doushi_x > -1:
            relWords_doushi = self.relWordsObj.get(words, 'doushi')
            titleWords[doushi_x] = relWords_doushi["ALL"][0]


        result =  str(' '.join(titleWords)).decode('string-escape')
        print(result)
