#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import create_title_pos_E as getpos
import calc_cos_sim as getwords
import random

<<<<<<< HEAD
word = ['エイリアン','隠し子']
=======
import sys
import codecs
import cgitb
>>>>>>> 7b753813028100375d618a78f764473bc9f259da

# load corpus
relatedWords = getwords.RelatedWords()
print "vectrized"
sys.stdout.flush()

# begin 
cgitb.enable()

sys.stdout.write("> ")
sys.stdout.flush()
#num = sys.stdin.readline()

print ('Content-type: text/html; charset=UTF-8')
print ("\r\n\r\n")
sys.stdout.flush()

#print num
#sys.stdout.flush()

#num = num.replace('\n','').strip()
num = 'num'

while num:
    word = ['エイリアン','隠し子']

    #print '<html>'
    #print '<body>'

    word_id = getwords.RelatedWords.wordsToIndex(relatedWords, word)

    titlePosObj = getpos.Title()

    for k in range(20):
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
            resultWord = getwords.RelatedWords.getWords(relatedWords,meishiWords, word, 'meishi', len(meishi_x))

            j = 0
            for idx in meishi_x:
                titleWords[idx] = resultWord[j]
                j += 1
         
            if doushi_x > -1:
                resultWord2 = getwords.RelatedWords.getWords(relatedWords,meishiWords, word, 'doushi', 1)
                titleWords[doushi_x] = resultWord2[0]
            print '#############<br />'
            print str(' '.join(titleWords)).decode('string-escape')
            print '<br />'
            sys.stdout.flush()
        except Exception as e:
            print '#############<br />'
            print str(e)
            print '<br />'
            sys.stdout.flush()

    print '</body>'
    print '</html>'

    sys.stdout.write("> ")
    sys.stdout.flush()
    #num = sys.stdin.readline()
    #originalQ = num
    #num = num.replace('\n','').strip()
    num = 'num'

getwords.RelatedWords.close(relatedWords)
    
     
