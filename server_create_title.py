#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import create_title_pos_E as getpos
import calc_cos_sim as getwords
import random
import socket
import sys
import codecs
import cgitb

host = "172.31.57.200"
port = 10002

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind((host,port)) 
serversock.listen(10) 

# load corpus
relatedWords = getwords.RelatedWords()

while True:
    #getwords.RelatedWords.close(relatedWords)
    clientsock, client_address = serversock.accept()
    rcvmsg = clientsock.recv(1024)
    if rcvmsg == '':
        break
    word = rcvmsg.split(',')
    word_out = ''    
    #getwords.RelatedWords.open(relatedWords)

    word_id = getwords.RelatedWords.wordsToIndex(relatedWords, word)
    titlePosObj = getpos.Title()

    for k in range(1):
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
            word_out = word_out + str(' '.join(titleWords)).decode('string-escape')
            word_out = word_out + '<br />'
        except Exception as e:
            word_out = word_out

    clientsock.sendall(word_out)
    clientsock.close()
    #getwords.RelatedWords.close(relatedWords)
    
     
