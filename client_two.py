"""
A simple Python script to send messages with bluethooth.
"""

import socket

hostMACAddress = 'DC:A6:32:35:20:0F' # De MAC address van de Bluetooth adapter op de server. (Dus de pie die de data ontvangt. Het kan ook b$
port = 4 # 3 is keuze die je zelf kan maken. Wel moet de port hetzelfde zijn als bij de client script.
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)

while id != 914171570937 and id != 848246612969:

        import time
        import RPi.GPIO as GPIO
        from mfrc522 import SimpleMFRC522

        reader = SimpleMFRC522()

        GPIO.setwarnings(False)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(37, GPIO.OUT)
        GPIO.output(37, GPIO.LOW)
        GPIO.output(12, GPIO.HIGH)

        id, text = reader.read()
        print(id)

        if id == 914171570937:
                GPIO.output(12, GPIO.LOW)
                serverMACAddress = 'DC:A6:32:32:BF:4B' #addres van de ontvannger pi
                port = 4
                s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
                s.connect((serverMACAddress,port))
                goed = 1
                sendg = str(goed)
                s.send(bytes(sendg, 'UTF-8'))
                s.close()s.send(bytes(send1, 'UTF-8'))
                s.close()


        elif id == 848246612969:

                GPIO.output(12, GPIO.LOW)
                start_time = time.time()
                seconds = 4

                while True:
                        current_time = time.time()
                        elapsed_time = current_time - start_time
                        GPIO.output(37, GPIO.HIGH)
                        time.sleep(0.1)
                        GPIO.output(37, GPIO.LOW)
                        time.sleep(0.1)

                        if elapsed_time > seconds:
                                serverMACAddress = 'DC:A6:32:32:BF:4B' #addres van de ontvannger pi
                                port = 4
                                s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
                                s.connect((serverMACAddress,port))
                                fout = 0
                                sendf = str(fout)
                                s.send(bytes(sendf, 'UTF-8'))
                                s.close()s.send(bytes(send1, 'UTF-8'))
                                s.close()
                                break

        else:

                start_time = time.time()
                seconds = 4

                while True:
                        current_time = time.time()
                        elapsed_time = current_time - start_time

                        GPIO.output(37, GPIO.HIGH)
                        GPIO.output(12, GPIO.HIGH)
                        time.sleep(0.1)
                        GPIO.output(37, GPIO.LOW)
                        GPIO.output(12, GPIO.LOW)
                        time.sleep(0.1)

                        if elapsed_time > seconds:      
                                break

GPIO.cleanup()