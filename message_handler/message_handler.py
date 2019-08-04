import logging
import threading
from queue import Queue, Empty
import json
import esc_controller as mc


class MessageHandler(threading.Thread):

    def __init__(self, receive_queue: Queue, transmit_queue: Queue, motor_controller: mc):

        threading.Thread.__init__(self)
        self.receive_queue  = receive_queue
        self.transmit_queue = transmit_queue
        self.motor_controller = motor_controller
        self.running = True

        self.logger = logging.getLogger('MessageHandler')
        self.logger.debug('__init__')

    def stop(self):
        self.running = False

    def run(self):

        while self.running:

            try:
                # get received message
                ret_q = self.receive_queue.get(True, 1000)
                self.logger.info("received msg")

                # clean up message
                msg = str(ret_q, 'utf-8').rstrip("\r\n")

                # parse message
                self.message_parser(msg)

            except Empty:
                continue

    def flight_parser(self, message):
        self.logger.info("parsing flight info")
        self.logger.info(message)

    def message_parser(self, message: str):

        try:
            msg = json.loads(message)
            self.logger.info(msg)

            if msg["messageId"] == "flight":
                self.flight_parser(msg)
        except KeyError as ke:
            self.logger.error(ke)
        except json.decoder.JSONDecodeError as e:
            self.logger.error(e)


