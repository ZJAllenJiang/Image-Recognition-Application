#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import cgi, os
import cgitb;
import socket
import sys
import struct
import time

cgitb.enable()
form = cgi.FieldStorage()

def image_client(fn):
    try:
        # client connects to the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # get server ip
        s.connect(('128.163.233.171', 58005))

    except socket.error as msg:
        print(msg)
        print(sys.exit(1))

    filepath=fn

    # preprocess input image and fit for transmission
    processed_file = struct.pack(b'128sq', bytes(os.path.basename(filepath), encoding='utf-8'), os.stat(filepath).st_size)
    s.send(processed_file)

    fp = open(filepath, 'rb')
    while True:
        data = fp.read(1024)
        if not data:
            #print('{0} sent.'.format(filepath))
            break
        s.send(data)
    pred = s.recv(1024).decode()
    s.close()
    return pred
start = time.time()

fileitem = form['filename']

if fileitem.filename:
   fn = os.path.basename(fileitem.filename.replace("\\", "/" ))
   open(os.getcwd()+'/' + fn,'wb').write(fileitem.file.read())
   message = fn

else:
   message = 'no file'

pred = image_client(fn)

end = time.time()

t = end - start
t = round(t,3)

fsize = os.path.getsize(fn)
fsize = fsize/float(1024*1024) * 1024
fsize = round(fsize, 2)

print('Content-type:text/html \n\n')
print('<p style="text-align:center;font-size:20px;"> %s</p>' % message)
print('<div align="center"> <img src=%s height="300" align="middle"></img> </div>' % fn)
print('<p style="text-align:center;font-size:20px;">Result: %s</p>' % pred)
print('<p style="text-align:center;font-size:20px;">Time: %s s</p>' % t)
print('<p style="text-align:center;font-size:20px;">Size: %s KB</p>' % fsize)

