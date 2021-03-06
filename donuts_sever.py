#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import donuts_create_titles as gen
import random
import socket
import sys
import codecs
import cgitb

host = "172.31.57.200"
port = 10004

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind((host,port)) 
serversock.listen(10) 

# load corpus
titleObj = gen.Title()
inputObj = gen.Input()

while True :
    clientsock, client_address = serversock.accept()
    rcvmsg = clientsock.recv(8192)
    if rcvmsg == '':
       continue
    inputWords = inputObj.getMeishi(rcvmsg)

    word_out = ''    
    try:
        titles = titleObj.create(inputWords, 13)
	titles_donuts = titleObj.createDonuts(inputWords, 17 )

	titles_key =  list(titles.keys())
        titles_donuts_key =  list(titles_donuts.keys())

	titles_key.extend(titles_donuts_key)
	titles_key = random.sample(titles_key, len(titles_key))
	
	titles.update(titles_donuts)
	
	for key in titles_key:
	    word_out += ' > '		
	    word_out +=  str(key).decode('string-escape')
	    word_out += ' <br /> '
	    word_out += '  --- メッセージ・スコア : '
	    word_out += str(titles[key])
	    word_out += ' <br /> '
	    word_out += ' <br /> ' 	  

    except Exception as e:
	print(e)
        word_out = word_out

    clientsock.sendall(word_out)
    clientsock.close()
    
     
