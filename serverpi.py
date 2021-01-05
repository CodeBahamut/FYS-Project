import socket
import time

score = 0

start_time = time.time()
seconds = 300

while True:
    serverMACAddress = 'DC:A6:32:BC:EB:49'  # addres van de ontvannger pi
    port = 3
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.connect((serverMACAddress, port))

    send1 = str(score)
    print(send1)
    s.send(bytes(send1, 'UTF-8'))
    s.close()

    current_time = time.time()
    elapsed_time = current_time - start_time

    hostMACAddress = 'DC:A6:32:32:BF:4B'  # De MAC address van de Bluetooth adapter op de server. (Dus de pie die de data ontvangt. Het kan ook b$
    port = 3  # 3 is keuze die je zelf kan maken. Wel moet de port hetzelfde zijn als bij de client script.
    backlog = 1
    size = 1024
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.bind((hostMACAddress, port))
    s.listen(backlog)
    try:
        client, address = s.accept()
        while 1:
            data = client.recv(size)
            if data:
                score = int(data)
                print(data)  # Whatever je gestuurd hebt word geprint in console je kan dus ook hiermee een pin aan sturen met een if etc.
                client.send(data)
                if data == 1:
                    score = score + 1
    except:
        print("Closing socket")
        print(score)
        client.close()
        s.close()

    serverMACAddress = 'DC:A6:32:35:20:0F'  # addres van de ontvannger pi
    port = 4
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.connect((serverMACAddress, port))

    send2 = str(score)
    print(send2)
    s.send(bytes(send2, 'UTF-8'))
    s.close()

    hostMACAddress = 'DC:A6:32:32:BF:4B'  # De MAC address van de Bluetooth adapter op de server. (Dus de pie die de data ontvangt. Het kan ook b$
    port = 4  # 3 is keuze die je zelf kan maken. Wel moet de port hetzelfde zijn als bij de client script.
    backlog = 1
    size = 1024
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.bind((hostMACAddress, port))
    s.listen(backlog)
    try:
        client, address = s.accept()
        while 1:
            data = client.recv(size)
            if data:
                score = int(data)
                print(data)  # Whatever je gestuurd hebt word geprint in console je kan dus ook hiermee een pin aan sturen met een if etc.
                client.send(data)
                if data == 1:
                    score = score + 1
    except:
        print("Closing socket")
        print(score)
        client.close()
        s.close()

    if elapsed_time > seconds:
        break

print(score)
