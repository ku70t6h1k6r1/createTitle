#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
import socket
import sys
import codecs
import cgitb
# begin 
cgitb.enable()

print ('Content-type: text/html; charset=UTF-8')
print ("\r\n\r\n")
sys.stdout.flush()
#print 'waiting....'
#sys.stdout.flush()

for i in range(20):

    host = "172.31.57.200" 
    port = 10002
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client.connect((host, port))
    client.send("from nadechin") 
    response = client.recv(4096)
    print response
    sys.stdout.flush()
    client.close()
