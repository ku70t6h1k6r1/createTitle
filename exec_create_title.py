# -*- coding: utf-8 -*-
import create_title_pos_E as getpos
import random

titlePosObj = getpos.Title()

#繰り返す場合はここから
getpos.create(titlePosObj)
titlePos = getpos.create.titlePosA(titlePosObj)
titleWords = getpos.create.titleA(titlePosObj)

#名詞変換
meishiIndex = []
meishiWords = []
defaultIndex = [0,2]

meishi_x = [random.sample(defaultIndex,1)]
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
    meishiWords.append(idx)
    
 try:
    #meishi
    
 except:
    
 
