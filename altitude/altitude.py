from esc_controller import EscController
from queue import Queue, Empty
import threading
import json
import logging


class Altitude(threading.Thread):

    def __init__(self, receive_queue: Queue, esc_ctl: EscController):
        threading.Thread.__init__(self)
        self.receive_queue = receive_queue
        self.esc_ctl = esc_ctl
        self.running = True

        self.logger = logging.getLogger('Altitude')
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

    def flight_handler(self, message):
        self.logger.info("parsing flight info")
        self.logger.info(message)
        self.esc_ctl.set_thrust(message["throttle"])

    def arm_handler(self):
        self.esc_ctl.software_arm()

    def message_parser(self, message: str):
        try:
            msg = json.loads(message)
            self.logger.info(msg)

            if msg["messageId"] == "flight":
                self.flight_handler(msg)
            if msg["messageId"] == "arm":
                self.arm_handler()

        except KeyError as ke:
            self.logger.error(ke)
        except json.decoder.JSONDecodeError as e:
            self.logger.error(e)
