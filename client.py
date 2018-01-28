#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
import socket
import sys
import codecs
import cgitb
import cgi

# begin 
cgitb.enable()

print ('Content-type: text/html; charset=UTF-8')
print ("\r\n\r\n")
sys.stdout.flush()

form = cgi.FieldStorage()
words = form["senddata"].value
words = str(words) #unicode(words,"utf-8")

print("<h2>{0} に関するタイトル案</h2>".format(words))
print("<a href=\"./index.rb\">戻る</a>")
print("<p></p>")

for i in range(20):

    host = "172.31.57.200" 
    port = 10002
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client.connect((host, port))
    client.send(words) 
    response = client.recv(4096)
    print response
    sys.stdout.flush()
    client.close()
