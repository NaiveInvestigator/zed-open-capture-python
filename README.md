# zed-open-capture-python

Python bindings for [stereolabs/zed-open-capture](https://github.com/stereolabs/zed-open-capture) sensor capture API.

## Install

```bash
git clone https://github.com/NaiveInvestigator/zed-open-capture-python
cd zed-open-capture-python
make
```

This will:
1. Install system prerequisites (`make deps`, one-time, needs sudo)
2. Clone and build `zed-open-capture`
3. Install the udev rule for USB HID sensor access (needs sudo, replug camera after)
4. Build and install the Python bindings + wrapper

## Usage

```python
from zed_sensors import ZedSensors

sens = ZedSensors()
sens.initialize_sensors()
print(sens.get_serial_number())

imu = sens.get_last_imu_data()
print(imu["accel"], imu["gyro"])
```

See `examples/sensors_example.py` for a full example.

## Requirements

- ZED 2i / ZED 2 / ZED Mini camera
- Linux, GCC 7.5+, CMake 3.15+
- Run `make deps` once if you don't already have build tools / libusb / hidapi
