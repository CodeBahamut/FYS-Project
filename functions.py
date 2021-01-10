import config
import time
import socket
import mysql.connector as connector

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
Database related functions
'''


def connect_db():
    db = config.db_config

    try:
        c = connector.connect(**db)
        print("Connected!")
        return c
    except:
        print("Cant connect to db")


def save_data(name, score):
    db = connect_db()
    cursor = db.cursor()
    sql = "INSERT INTO Fys (name, score) VALUES (%s, %s)"
    val = (name, score)

    cursor.execute(sql, val)
    db.commit()
    save_data()


def get_scores():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT`name`, `score` FROM`Fys`")

    result = cursor.fetchall()

    return result


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
