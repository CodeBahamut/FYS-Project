"""
A simple Python script to receive messages from client
"""

import socket

hostMACAddress = '00:1f:e1:dd:08:3d' # De MAC address van de Bluetooth adapter op de server. (Dus de pie die de data ontvangt. Het kan ook bijde kante op maar dan heb je een method nodig. :)
port = 3 # 3 is keuze die je zelf kan maken. Wel moet de port hetzelfde zijn als bij de client script.
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)
try:
    client, address = s.accept()
    while 1:
        data = client.recv(size)
        if data:
            print(data)  # Whatever je gestuurd hebt word geprint in console je kan dus ook hiermee een pin aan sturen met een if etc.
            client.send(data)
except:
    print("Closing socket")
    client.close()
    s.close()
