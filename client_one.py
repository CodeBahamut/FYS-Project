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
                score = score +1
                print(score)


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
send1 = str(score)
print(send1)
s.send(bytes(send1, 'UTF-8'))
s.close()