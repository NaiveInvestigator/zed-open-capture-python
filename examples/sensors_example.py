#!/usr/bin/env python3
"""Simple test script for the ZedSensors wrapper."""

from zed_sensors import ZedSensors

def main():
    print("hewwo")

    sens = ZedSensors(verbosity="info")
    sens.initialize_sensors()  # auto-picks first available device

    print(f"Connected to camera sn: {sens.get_serial_number()}")
    print(f"Firmware version: {sens.get_firmware_version()}")

    last_imu_ts = 0

    for i in range(100):
        imu = sens.get_last_imu_data(5000)
        if imu["valid"]:
            print(f"\n**** New IMU data [{i}] ****")
            print(f" * Timestamp: {imu['timestamp']} nsec")
            if last_imu_ts:
                freq = 1e9 / (imu["timestamp"] - last_imu_ts)
                print(f" * Frequency: {freq:.1f} Hz")
            last_imu_ts = imu["timestamp"]
            print(f" * Accel [m/s²]: {imu['accel']}")
            print(f" * Gyro  [°/s]: {imu['gyro']}")

        mag = sens.get_last_magnetometer_data(100)
        if mag["valid"]:
            print(f" * Mag field [uT]: {mag['field']}")

        env = sens.get_last_environment_data(100)
        if env["valid"]:
            print(f" * Pressure: {env['pressure']} hPa, "
                  f"Temp: {env['temperature']} °C, "
                  f"Humidity: {env['humidity']} %rH")

        temp = sens.get_last_camera_temperature_data(100)
        if temp["valid"]:
            print(f" * Cam Temp L/R: {temp['temp_left']} / {temp['temp_right']} °C")


if __name__ == "__main__":
    main()
