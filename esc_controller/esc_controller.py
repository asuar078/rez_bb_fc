from esc_controller import esc_const
from time import sleep
import logging
from enum import Enum

import rcpy
import rcpy.servo as servo
import rcpy.clock as clock


class EscState(Enum):
    IDLE = 0
    ARMED = 1


class EscController:
    UPDATE_PERIOD = 1.0 / 300.0

    state = EscState.IDLE

    def __init__(self):

        # set state to rcpy.RUNNING
        rcpy.set_state(rcpy.RUNNING)

        # front esc
        self.front_right = servo.ESC(esc_const.EscPwmPins.FRONT_RIGHT)
        self.front_left = servo.ESC(esc_const.EscPwmPins.FRONT_LEFT)

        # back esc
        self.back_right = servo.ESC(esc_const.EscPwmPins.BACK_RIGHT)
        self.back_left = servo.ESC(esc_const.EscPwmPins.BACK_LEFT)

        self.logger = logging.getLogger('MotorController')
        self.logger.debug('__init__')

        # create clock to do periodic updates
        self.fr_clock = clock.Clock(self.front_right, self.UPDATE_PERIOD)
        self.fl_clock = clock.Clock(self.front_left, self.UPDATE_PERIOD)
        self.br_clock = clock.Clock(self.back_right, self.UPDATE_PERIOD)
        self.bl_clock = clock.Clock(self.back_left, self.UPDATE_PERIOD)

        # set all to zero
        self.front_right.set(0)
        self.front_left.set(0)
        self.back_right.set(0)
        self.back_left.set(0)

        # start all the clocks
        self.fr_clock.start()
        self.fl_clock.start()
        self.br_clock.start()
        self.bl_clock.start()

    def __del__(self):
        self.fr_clock.stop()
        self.fl_clock.stop()
        self.br_clock.stop()
        self.bl_clock.stop()

    def software_arm(self):
        if self.state == EscState.IDLE:
            self.logger.info("starting arming sequence")
            self.front_right.set(-0.1)
            self.front_left.set(-0.1)
            self.back_right.set(-0.1)
            self.back_left.set(-0.1)
            sleep(2)
            self.logger.info("ending arming sequence")

            self.front_left.set(0)
            self.back_right.set(0)
            sleep(2)

            self.state = EscState.ARMED
        else:
            self.logger.info("esc already armed")

    def set_thrust(self, duty):
        if self.state == EscState.ARMED:
            mapped_duty = esc_const.map_val(abs(duty))
            if 0 <= mapped_duty <= 1:
                self.front_right.set(mapped_duty)
                self.front_left.set(mapped_duty)
                self.back_right.set(mapped_duty)
                self.back_left.set(mapped_duty)
            else:
                raise ValueError("duty cycle out of range {}".format(duty))
        else:
            self.logger.error("must arm esc before using")

    def test_ramp(self):

        self.logger.info("test ramping ")
        for x in range(0, 25, 1):
            self.front_left.set(x / 100.0)
            self.back_right.set(x / 100.0)
            self.logger.info("speed: {}".format(x))
            sleep(1)

        for x in range(24, 0, -1):
            self.front_left.set(x / 100.0)
            self.back_right.set(x / 100.0)
            self.logger.info("speed: {}".format(x))
            sleep(1)
