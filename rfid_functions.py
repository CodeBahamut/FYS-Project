from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import functions
import config
import time


def get_id():
    reader = SimpleMFRC522()

    GPIO.setwarnings(False)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(37, GPIO.OUT)
    GPIO.output(37, GPIO.LOW)
    GPIO.output(12, GPIO.HIGH)

    id, text = reader.read()
    print(id)
    GPIO.cleanup()
    return id


def scan_card_and_send_score(id):
    if id == 914171570937:
        GPIO.output(12, GPIO.LOW)
        functions.blue_send_msg(config.robot_mac, config.robot_port, config.score_add_point)

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
                functions.blue_send_msg(config.robot_mac, config.robot_port, config.score_no_point)
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
                GPIO.cleanup()
                break
