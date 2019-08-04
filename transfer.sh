#!/usr/bin/env bash

USER=debian
PASSWORD="temppwd"

IP_ADDR=192.168.1.201
TRANSFER_DIR=/home/debian/rez_bb_fc

# application
sshpass -p ${PASSWORD} scp flight_controller.py ${USER}@${IP_ADDR}:${TRANSFER_DIR}
sshpass -p ${PASSWORD} scp -r esc_controller ${USER}@${IP_ADDR}:${TRANSFER_DIR}
#sshpass -p ${PASSWORD} scp -r message_handler ${USER}@${IP_ADDR}:${TRANSFER_DIR}
sshpass -p ${PASSWORD} scp -r communication_server ${USER}@${IP_ADDR}:${TRANSFER_DIR}
sshpass -p ${PASSWORD} scp -r altitude ${USER}@${IP_ADDR}:${TRANSFER_DIR}

# scripts
#sshpass -p ${PASSWORD} scp configure_pins.sh ${USER}@${IP_ADDR}:${TRANSFER_DIR}
