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
    rcvmsg = clientsock.recv(1024)
    if rcvmsg == '':
       continue
    inputWords = inputObj.getMeishi(rcvmsg)

    word_out = ''    
    try:
        titles = titleObj.create(inputWords, 20)
	titles_donuts = titleObj.createDonuts(inputWords, 10 )
	titles.extend(titles_donuts)
	titles = random.sample(titles, len(titles))
	word_out += '>'
	word_out +=  str('<br /> >'.join(titles)).decode('string-escape')
 	  
        word_out = word_out + '<br />'
    except Exception as e:
	print(e)
        word_out = word_out

    clientsock.sendall(word_out)
    clientsock.close()
    
     
