#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
import socket
import sys
import codecs
import cgitb
import cgi
import subprocess


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

error = 0
title_n = 0

for i in range(20):

    try:
        host = "172.31.57.200" 
        port = 10003
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        client.connect((host, port))
        client.send(words) 
        response = client.recv(4096)
        print response
        sys.stdout.flush()
        if response != "":
            title_n += 1

        client.close()

    except:
        error +=1
        break

if error > 0:
    print "TCPサーバーが停止しています。<br />"
    cmd = "python /usr/local/apache/cgi-bin/createTitle/server_create_title.py &"
    returncode = subprocess.Popen(cmd, shell=True )
    print "再起動中です。1分ほどおいて再度試してください。<br />"
elif title_n < 1:
    print "入力された単語を知りません。"

else:
    print "end"
