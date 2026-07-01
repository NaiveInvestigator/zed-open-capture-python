#!/usr/bin/env python3
"""List all available ZED camera devices."""

from zed_sensors import ZedSensors

def main():
    sens = ZedSensors(verbosity="info")
    devices = sens.get_device_list()
    
    print(f"\nFound {len(devices)} device(s):")
    for device_id in devices:
        print(f"  - Serial Number: {device_id}")
    
    if devices:
        print(f"\nConnecting to first device (SN: {devices[0]})...")
        if sens.initialize_sensors(devices[0]):
            sn = sens.get_serial_number()
            fw_major, fw_minor = sens.get_firmware_version()
            print(f"Connected successfully!")
            print(f"  Serial Number: {sn}")
            print(f"  Firmware Version: {fw_major}.{fw_minor}")
        else:
            print("Failed to initialize sensors")
    else:
        print("No devices found. Please connect a ZED camera.")

if __name__ == "__main__":
    main()
