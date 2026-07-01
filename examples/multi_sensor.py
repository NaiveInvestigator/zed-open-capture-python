#!/usr/bin/env python3
"""Collect and display all sensor data in a structured format."""

from zed_sensors import ZedSensors
import time

class SensorDataCollector:
    """Helper class to organize sensor data collection."""
    
    def __init__(self):
        self.sens = ZedSensors(verbosity="error")
        self.last_update_times = {
            "imu": 0,
            "mag": 0,
            "env": 0,
            "temp": 0
        }
        self.latest_data = {
            "imu": None,
            "mag": None,
            "env": None,
            "temp": None
        }
    
    def initialize(self, device_id=None):
        """Initialize the sensor."""
        if not self.sens.initialize_sensors(device_id or -1):
            return False
        
        sn = self.sens.get_serial_number()
        fw_major, fw_minor = self.sens.get_firmware_version()
        print(f"Initialized: SN={sn}, FW={fw_major}.{fw_minor}")
        return True
    
    def update(self):
        """Collect latest data from all sensors."""
        current_time = time.time()
        
        # Update IMU (highest frequency)
        imu = self.sens.get_last_imu_data(timeout_usec=5000)
        if imu["valid"]:
            self.latest_data["imu"] = imu
            self.last_update_times["imu"] = current_time
        
        # Update magnetometer
        mag = self.sens.get_last_magnetometer_data(timeout_usec=100)
        if mag["valid"]:
            self.latest_data["mag"] = mag
            self.last_update_times["mag"] = current_time
        
        # Update environment
        env = self.sens.get_last_environment_data(timeout_usec=100)
        if env["valid"]:
            self.latest_data["env"] = env
            self.last_update_times["env"] = current_time
        
        # Update camera temperature
        temp = self.sens.get_last_camera_temperature_data(timeout_usec=100)
        if temp["valid"]:
            self.latest_data["temp"] = temp
            self.last_update_times["temp"] = current_time
    
    def print_status(self):
        """Print all available sensor data."""
        # IMU data
        if self.latest_data["imu"]:
            imu = self.latest_data["imu"]
            print(f"  IMU (updated {time.time() - self.last_update_times['imu']:.2f}s ago):")
            print(f"    Accel: X={imu['accel'][0]:7.3f} Y={imu['accel'][1]:7.3f} Z={imu['accel'][2]:7.3f} m/s²")
            print(f"    Gyro:  X={imu['gyro'][0]:7.3f} Y={imu['gyro'][1]:7.3f} Z={imu['gyro'][2]:7.3f} °/s")
        
        # Magnetometer data
        if self.latest_data["mag"]:
            mag = self.latest_data["mag"]
            print(f"  Magnetometer (updated {time.time() - self.last_update_times['mag']:.2f}s ago):")
            print(f"    Field: X={mag['field'][0]:7.3f} Y={mag['field'][1]:7.3f} Z={mag['field'][2]:7.3f} µT")
        
        # Environment data
        if self.latest_data["env"]:
            env = self.latest_data["env"]
            print(f"  Environment (updated {time.time() - self.last_update_times['env']:.2f}s ago):")
            print(f"    Temperature: {env['temperature']:7.2f} °C")
            print(f"    Pressure:    {env['pressure']:7.2f} hPa")
            print(f"    Humidity:    {env['humidity']:7.2f} %rH")
        
        # Camera temperature
        if self.latest_data["temp"]:
            temp = self.latest_data["temp"]
            print(f"  Camera Temp (updated {time.time() - self.last_update_times['temp']:.2f}s ago):")
            print(f"    Left:  {temp['temp_left']:7.2f} °C")
            print(f"    Right: {temp['temp_right']:7.2f} °C")

def main():
    print("Multi-Sensor Data Collection\n")
    
    collector = SensorDataCollector()
    
    print("Initializing sensors...")
    if not collector.initialize():
        print("Failed to initialize")
        return
    
    print("\nCollecting sensor data (20 seconds)...\n")
    
    start_time = time.time()
    update_count = 0
    
    try:
        while time.time() - start_time < 20:
            collector.update()
            update_count += 1
            
            # Print status every 5 updates
            if update_count % 5 == 0:
                print(f"--- Update #{update_count} @ {time.time() - start_time:.1f}s ---")
                collector.print_status()
                print()
            
            time.sleep(0.1)  # Small delay to avoid CPU spinning
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    
    elapsed = time.time() - start_time
    print(f"Collection complete: {update_count} updates in {elapsed:.1f}s")

if __name__ == "__main__":
    main()
