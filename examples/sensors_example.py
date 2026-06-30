#!/usr/bin/env python3
from zed_sensors import ZedSensors

def main():
    sens = ZedSensors(verbosity="info")
    sens.initialize_sensors()

    print(f"Connected to camera sn: {sens.get_serial_number()}")
    print(f"Firmware: {sens.get_firmware_version()}")

    last_imu_ts = 0
    for _ in range(4000):
        imu = sens.get_last_imu_data(5000)
        if imu["valid"]:
            print(f"IMU ts={imu['timestamp']} accel={imu['accel']} gyro={imu['gyro']}")
            last_imu_ts = imu["timestamp"]

if __name__ == "__main__":
    main()
