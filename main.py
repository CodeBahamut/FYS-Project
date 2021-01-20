from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL
from celery import Celery
from datetime import timedelta
import config
import functions
import control_management
from multiprocessing import Process


def game_start(username):
    config.controls_inactive = False
    game_score = 0

    control_management.find_controller()
    controller = control_management.MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller_process = Process(target=controller.listen, name="Listen_to_controller")
    distance_check_process = Process(target=control_management.check_distance, name="Check_car_distance")
    time_limit_reached_process = Process(target=functions.countdown, args=config.game_time_length_sec)

    controller_process.daemon = True
    time_limit_reached_process.daemon = True
    distance_check_process.daemon = True

    controller_process.start()
    time_limit_reached_process.start()
    distance_check_process.start()

    while True:
        if config.game_stop:
            cursor = mysql.cursor()
            sql = "INSERT INTO Fys (name, score) VALUES (%s, %s)"
            val = (username, game_score)

            cursor.execute(sql, val)
            mysql.commit()

            if controller_process.is_alive():
                controller_process.close()
            if time_limit_reached_process.is_alive():
                time_limit_reached_process.close()
            if distance_check_process.is_alive():
                distance_check_process.close()
            break

        functions.blue_send_msg(config.client_one_mac, config.client_one_port, config.is_inactive)
        functions.blue_send_msg(config.client_two_mac, config.client_two_port, config.is_active)

        game_score += functions.blue_receive_msg(config.client_two_mac, config.robot_port)

        functions.blue_send_msg(config.client_one_mac, config.client_one_port, config.is_active)
        functions.blue_send_msg(config.client_two_mac, config.client_two_port, config.is_inactive)

        game_score += functions.blue_receive_msg(config.client_one_mac, config.robot_port)


if __name__ == "__main__":
    functions.MySocket.connect(config.website_ip, config.robot_port)
    username = functions.MySocket.receive_data()
    game_process = Process(target=game_start(username))
