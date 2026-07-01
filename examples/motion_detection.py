#!/usr/bin/env python3
"""Detect motion by monitoring acceleration magnitude."""

from zed_sensors import ZedSensors
import math
import time

def accel_magnitude(accel):
    """Calculate magnitude of acceleration vector."""
    return math.sqrt(accel[0]**2 + accel[1]**2 + accel[2]**2)

def main():
    sens = ZedSensors(verbosity="error")
    
    print("Initializing sensors...")
    if not sens.initialize_sensors():
        print("Failed to initialize sensors")
        return
    
    print(f"Connected to camera SN: {sens.get_serial_number()}")
    print("\nCalibrating static acceleration (5 seconds)...")
    
    # Calibrate: record static acceleration (should be ~9.81 m/s² from gravity)
    static_samples = []
    start = time.time()
    while time.time() - start < 5:
        imu = sens.get_last_imu_data(timeout_usec=5000)
        if imu["valid"]:
            mag = accel_magnitude(imu["accel"])
            static_samples.append(mag)
    
    if not static_samples:
        print("No IMU data received during calibration")
        return
    
    baseline = sum(static_samples) / len(static_samples)
    print(f"Baseline acceleration: {baseline:.3f} m/s² (from {len(static_samples)} samples)")
    print(f"Standard deviation: {math.sqrt(sum((x - baseline)**2 for x in static_samples) / len(static_samples)):.3f} m/s²")
    
    # Motion detection threshold: 1.5x the baseline
    motion_threshold = baseline * 1.5
    print(f"Motion detection threshold: {motion_threshold:.3f} m/s²")
    print("\nMonitoring for motion (30 seconds)...")
    print("(Device should remain still for the first 5 seconds)")
    print()
    
    motion_events = []
    motion_detected = False
    start = time.time()
    
    while time.time() - start < 30:
        imu = sens.get_last_imu_data(timeout_usec=5000)
        
        if imu["valid"]:
            mag = accel_magnitude(imu["accel"])
            
            # Detect motion
            if mag > motion_threshold and not motion_detected:
                motion_detected = True
                elapsed = time.time() - start
                motion_events.append({
                    "time": elapsed,
                    "accel_mag": mag,
                    "accel": imu["accel"]
                })
                print(f"[{elapsed:6.2f}s] MOTION DETECTED! Accel magnitude: {mag:.3f} m/s²")
                print(f"               Accel vector: ({imu['accel'][0]:.3f}, {imu['accel'][1]:.3f}, {imu['accel'][2]:.3f})")
            
            elif mag < motion_threshold and motion_detected:
                motion_detected = False
                elapsed = time.time() - start
                print(f"[{elapsed:6.2f}s] Motion stopped. Accel magnitude: {mag:.3f} m/s²")
    
    print(f"\nMotion Detection Summary:")
    print(f"  Total motion events: {len(motion_events)}")
    if motion_events:
        print(f"  First motion at: {motion_events[0]['time']:.2f}s")
        print(f"  Peak acceleration: {max(e['accel_mag'] for e in motion_events):.3f} m/s²")

if __name__ == "__main__":
    main()
