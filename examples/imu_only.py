#!/usr/bin/env python3
"""Collect IMU data only and demonstrate real-time frequency calculation."""

from zed_sensors import ZedSensors
import time

def main():
    sens = ZedSensors(verbosity="error")
    
    print("Initializing sensors...")
    if not sens.initialize_sensors():
        print("Failed to initialize sensors")
        return
    
    print(f"Connected to camera SN: {sens.get_serial_number()}")
    print("Collecting IMU data for 10 seconds...\n")
    
    imu_count = 0
    start_time = time.time()
    last_imu_ts = None
    
    while time.time() - start_time < 10:
        imu = sens.get_last_imu_data(timeout_usec=5000)
        
        if imu["valid"]:
            imu_count += 1
            
            # Calculate frequency if we have a previous timestamp
            if last_imu_ts is not None:
                dt_sec = (imu["timestamp"] - last_imu_ts) / 1e9
                freq = 1.0 / dt_sec if dt_sec > 0 else 0
                print(f"[{imu_count:3d}] Freq: {freq:7.1f} Hz | "
                      f"Accel: ({imu['accel'][0]:7.3f}, {imu['accel'][1]:7.3f}, {imu['accel'][2]:7.3f}) m/s²")
            else:
                print(f"[{imu_count:3d}] Accel: ({imu['accel'][0]:7.3f}, {imu['accel'][1]:7.3f}, {imu['accel'][2]:7.3f}) m/s²")
            
            last_imu_ts = imu["timestamp"]
    
    elapsed = time.time() - start_time
    avg_freq = imu_count / elapsed if elapsed > 0 else 0
    print(f"\nCollected {imu_count} samples in {elapsed:.1f}s")
    print(f"Average frequency: {avg_freq:.1f} Hz")

if __name__ == "__main__":
    main()
