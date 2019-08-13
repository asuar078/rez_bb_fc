import threading
import json
import logging
from queue import Queue, Empty
import rcpy.mpu9250 as mpu9250
import time


class ImuReader(threading.Thread):

    def __init__(self, data_queue: Queue):
        super().__init__()
        self.receive_queue = data_queue
        self.running = True

        self.logger = logging.getLogger('ImuReader')
        self.logger.debug('__init__')

        self.imu = mpu9250.IMU(enable_dmp=True,
                               dmp_sample_rate=10,
                               enable_magnetometer=True,
                               enable_fusion=True)

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            imu_reading = self.imu.read()
            imu_reading["messageId"] = "imu"
            self.logger.info("imu reading")
            self.logger.info(imu_reading)
            time.sleep(1.0 / 10.0)
