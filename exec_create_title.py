#!/usr/lib/python2.7
# -*- coding: utf-8 -*-
import create_title_pos_E as getpos
import calc_cos_sim　as getwords
import random

word = ['恋愛','変態']

relatedWords = getwords.RelatedWords()
word_id = getwords.RelatedWords.wordsToIndex(relatedWords, word)

titlePosObj = getpos.Title()

outTitles = {}
for i in range(20):
    getpos.Title.create(titlePosObj)
    titlePos = getpos.Title.titlePosA(titlePosObj)
    titleWords = getpos.Title.titleA(titlePosObj)

    #名詞変換
    meishiIndex = []
    meishiWords = []
    defaultIndex = [0,2]

    meishi_x = random.sample(defaultIndex,1)
    doushi_x = -1

    i = 0
    for pos in titlePos:
        if pos == '名詞':
            meishiIndex.append( i )
        elif pos == 'x_meishi':
            meishi_x.append( i )
        elif pos == 'x_doushi':
            doushi_x = i
        i += 1
    
    for idx in meishiIndex:
        meishiWords.append(titleWords[idx])
    
    try:
        #meishi
        resultWord = getwords.relatedWords.getWords(meishiWords, word, 'meishi', len(meishi_x))
        
        j = 0
        for idx in meishi_x:
            titleWords[idx] = resultWord[j]
            j += 1
         
        if doushi_x > -1:
            resultWord2 = getwords.relatedWords.getWords(meishiWords, word, 'doushi', 1)
            titleWords[doushi_x] = resultWord2[0] 
            print "#############" #str(RelatedWords.indexToWords(test, result["words"])).decode('string-escape')
            print titleWords
    except:
    
 
