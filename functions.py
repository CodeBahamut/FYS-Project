import time
import socket


'''
A  Python script to send and receive messages with bluethooth.

-IMPORTANT-
Port can be any number between 1 - 30 you want,
however it has to be the same as the one of the client where you are sending it to.
'''
size = 1024
backlog = 1


def blue_send_msg(server_mac_address, port, value):
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.connect((server_mac_address, port))
    s.send(bytes(value, 'UTF-8'))
    s.close()


def blue_receive_msg(host_mac_address, port):
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.bind((host_mac_address, port))
    s.listen(backlog)
    try:
        client, address = s.accept()
        while 1:
            data = client.recv(size)
            if data:
                print(data)  # Prints data that you received
                client.send(data)
                return data
    except:
        print("Closing socket")
        client.close()
        s.close()


'''
Game time function
'''


def countdown(t):
    while t:
        minutes, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(minutes, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1

    return True


class MySocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send_data(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def receive_data(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)
