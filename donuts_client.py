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
words_fix = words.replace("\n", "<br />")
print("<h1>咳暁夫AI</h1>")
print("<p><a href=\"./index_donut.rb\">戻る</a></p>")
print("<b>{0}</b>".format(words_fix))
print(" について以下、咳暁夫AIのコメント")

print("<p></p>")

error = 0
title_n = 0

for i in range(1):
    try:
        host = "172.31.57.200" 
        port = 10004
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        client.connect((host, port))
        client.send(words) 
        response = client.recv(8192)
        print "------------------------------------<br />"
        print response
        sys.stdout.flush()
        if response != "":
            title_n += 1

        client.close()

    except :
        error +=1
        break

if error > 0:
    print "TCPサーバーが停止しています。<br />"
    cmd = "python /usr/local/apache/cgi-bin/createTitle/donuts_sever.py &"
    returncode = subprocess.Popen(cmd, shell=True )
    print "再起動中です。1分ほどおいて再度試してください。<br />"
elif title_n < 1:
    print ">私は何も知りません。"

else:
    print "<br />------------------------------------"
