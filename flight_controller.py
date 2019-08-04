import logging
import time

import communication_server.control_server as cs
import message_handler as mh
import esc_controller as mc
import altitude
import queue

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )

CONTROL_SERVER_PORT_NUM = 1337


def main():
    server_receive_q = queue.Queue(15)
    server_transmit_q = queue.Queue(15)

    motors = mc.EscController()
    # motors = None
    server_thread = cs.ControlServerThread(CONTROL_SERVER_PORT_NUM, server_receive_q)

    # handler_thread = mh.MessageHandler(server_receive_q, server_transmit_q, motors)
    altitude_thread = altitude.Altitude(server_receive_q, motors)

    try:

        # motors = mc.EscController()
        # motors.software_arm()
        # motors.test_ramp()
        # motors.set_thrust(0.06)
        # time.sleep(20)

        logging.info("starting altitude thread")
        altitude_thread.start()

        logging.info("starting server thread")
        server_thread.start()

    except KeyboardInterrupt:

        altitude_thread.stop()
        altitude_thread.join(1000)

        server_thread.stop_server()
        server_thread.join(1000)


if __name__ == '__main__':
    main()
