#!/usr/bin/env python3
"""Demonstrate error handling and robust reconnection logic."""

from zed_sensors import ZedSensors
import time

def wait_for_device(max_attempts=30, timeout_sec=2):
    """Wait for a device to be available."""
    sens = ZedSensors(verbosity="error")
    
    for attempt in range(max_attempts):
        devices = sens.get_device_list()
        
        if devices:
            print(f"Device found on attempt {attempt+1}: SN {devices[0]}")
            return sens, devices[0]
        
        print(f"Waiting for device... (attempt {attempt+1}/{max_attempts})")
        time.sleep(timeout_sec)
    
    return None, None

def main():
    print("Sensor Data Collection with Reconnection\n")
    
    # Wait for device
    sens, device_id = wait_for_device()
    if not sens or device_id is None:
        print("ERROR: Could not find any device within timeout")
        return
    
    # Initialize
    print(f"\nInitializing device SN {device_id}...")
    if not sens.initialize_sensors(device_id):
        print("ERROR: Failed to initialize sensors")
        return
    
    sn = sens.get_serial_number()
    fw_major, fw_minor = sens.get_firmware_version()
    print(f"SUCCESS: Connected to SN {sn}, FW {fw_major}.{fw_minor}\n")
    
    # Collection loop with error handling
    sample_count = 0
    error_count = 0
    collection_time = 20  # seconds
    start_time = time.time()
    
    print(f"Collecting sensor data for {collection_time} seconds...")
    print("(Press Ctrl+C to stop)\n")
    
    try:
        while time.time() - start_time < collection_time:
            try:
                # Try to get IMU data
                imu = sens.get_last_imu_data(timeout_usec=5000)
                if imu["valid"]:
                    sample_count += 1
                    if sample_count % 100 == 0:  # Print every 100 samples
                        elapsed = time.time() - start_time
                        print(f"[{elapsed:6.1f}s] Collected {sample_count} samples (errors: {error_count})")
                
                # Try other sensors
                mag = sens.get_last_magnetometer_data(timeout_usec=100)
                env = sens.get_last_environment_data(timeout_usec=100)
                temp = sens.get_last_camera_temperature_data(timeout_usec=100)
                
            except Exception as e:
                error_count += 1
                print(f"ERROR collecting data: {e}")
                if error_count > 10:
                    print("Too many errors, attempting reconnection...")
                    if not sens.initialize_sensors(device_id):
                        print("Reconnection failed")
                        break
                    error_count = 0
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    
    elapsed = time.time() - start_time
    print(f"\nCollection Summary:")
    print(f"  Duration: {elapsed:.1f} seconds")
    print(f"  Samples: {sample_count}")
    print(f"  Errors: {error_count}")
    print(f"  Average rate: {sample_count/elapsed:.1f} samples/sec")

if __name__ == "__main__":
    main()
