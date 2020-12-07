"""
A simple Python script to send messages with bluethooth.
"""

import socket

serverMACAddress = '00:1f:e1:dd:08:3d' #addres van de ontvannger pi
port = 3
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))
while 1:
    text = input() #de text of whatever je wilt versturen
    if text == "quit":
        break
    s.send(bytes(text, 'UTF-8'))
s.close()