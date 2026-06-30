import numpy as np

import sensor_capture as sc


class ZedSensors:
    def __init__(self, verbosity: str = "ERROR"):
        """
        Initializes the ZED SensorCapture pipeline
        Args:
            verbosity: verbosity level case-insensitive (eg: "none", "error", "warning", "info")
        """
        self.supported_verbosity = {
            "NONE": sc.VERBOSITY.NONE,
            "ERROR": sc.VERBOSITY.ERROR,
            "WARNING": sc.VERBOSITY.WARNING,
            "INFO": sc.VERBOSITY.INFO,
        }
        eVerbosity = self.supported_verbosity[verbosity.upper()]
        # initialise sensor capture here
        self.sens = sc.SensorCapture(eVerbosity)

    def get_device_list(self) -> list:
        return self.sens.get_device_list()

    def initialize_sensors(self, device_id: int = None) -> bool:
        """
        Initializes sensors on a device. If device_id is None,
        automatically picks the first available device.
        """
        if device_id is None:
            devices = self.sens.get_device_list()
            assert len(devices) > 0, "No available ZED Mini or ZED2 cameras"
            device_id = devices[0]
        return self.sens.initialize_sensors(device_id)

    def get_serial_number(self) -> int:
        return self.sens.get_serial_number()

    def get_firmware_version(self) -> tuple:
        # returns (major, minor)
        return self.sens.get_firmware_version()

    def get_last_imu_data(self, timeout_usec: int = 5000) -> dict:
        """
        Returns a dict with keys: timestamp, valid, accel (np.ndarray[3]), gyro (np.ndarray[3])
        """
        d = self.sens.get_last_imu_data(timeout_usec)
        return {
            "timestamp": d.timestamp,
            "valid": d.valid == sc.IMU_NEW_VAL,
            "accel": np.array([d.aX, d.aY, d.aZ]),
            "gyro": np.array([d.gX, d.gY, d.gZ]),
        }

    def get_last_magnetometer_data(self, timeout_usec: int = 100) -> dict:
        d = self.sens.get_last_magnetometer_data(timeout_usec)
        return {
            "timestamp": d.timestamp,
            "valid": d.valid == sc.MAG_NEW_VAL,
            "field": np.array([d.mX, d.mY, d.mZ]),
        }

    def get_last_environment_data(self, timeout_usec: int = 100) -> dict:
        d = self.sens.get_last_environment_data(timeout_usec)
        return {
            "timestamp": d.timestamp,
            "valid": d.valid == sc.ENV_NEW_VAL,
            "pressure": d.press,
            "temperature": d.temp,
            "humidity": d.humid,
        }

    def get_last_camera_temperature_data(self, timeout_usec: int = 100) -> dict:
        d = self.sens.get_last_camera_temperature_data(timeout_usec)
        return {
            "timestamp": d.timestamp,
            "valid": d.valid == sc.TEMP_NEW_VAL,
            "temp_left": d.temp_left,
            "temp_right": d.temp_right,
        }
