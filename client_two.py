import functions
import config
import rfid_functions

while True:
    data = functions.blue_receive_msg(config.robot_mac, config.client_two_port)

    if data == config.is_active:
        card_id = rfid_functions.get_id()
        rfid_functions.check_and_send_score(card_id)
