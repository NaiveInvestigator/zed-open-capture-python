#include <pybind11/pybind11.h>
#include <pybind11/stl.h>          // for std::vector auto-conversion
#include "sensorcapture.hpp"

namespace py = pybind11;

PYBIND11_MODULE(sensor_capture, m) {
    m.doc() = "Python bindings for ZED SensorCapture";

    // ----> Bind the VERBOSITY enum
    py::enum_<sl_oc::VERBOSITY>(m, "VERBOSITY")
    .value("NONE",    sl_oc::VERBOSITY::NONE)
    .value("ERROR",   sl_oc::VERBOSITY::ERROR)
    .value("WARNING", sl_oc::VERBOSITY::WARNING)
    .value("INFO",    sl_oc::VERBOSITY::INFO)
    .export_values();
    // <---- Bind the VERBOSITY enum

    // ----> Bind IMU data struct
    py::class_<sl_oc::sensors::data::Imu>(m, "ImuData")
        .def_readonly("timestamp", &sl_oc::sensors::data::Imu::timestamp)
        .def_readonly("aX",        &sl_oc::sensors::data::Imu::aX)
        .def_readonly("aY",        &sl_oc::sensors::data::Imu::aY)
        .def_readonly("aZ",        &sl_oc::sensors::data::Imu::aZ)
        .def_readonly("gX",        &sl_oc::sensors::data::Imu::gX)
        .def_readonly("gY",        &sl_oc::sensors::data::Imu::gY)
        .def_readonly("gZ",        &sl_oc::sensors::data::Imu::gZ)
          .def_property_readonly("valid", [](const sl_oc::sensors::data::Imu &data) {
               return static_cast<int>(data.valid);
          })
        .def("__repr__", [](const sl_oc::sensors::data::Imu &d) {
            return "<ImuData ts=" + std::to_string(d.timestamp) + ">";
        });
    // <---- Bind IMU data struct

    // ----> Bind Magnetometer data struct
    py::class_<sl_oc::sensors::data::Magnetometer>(m, "MagnetometerData")
        .def_readonly("timestamp", &sl_oc::sensors::data::Magnetometer::timestamp)
        .def_readonly("mX",        &sl_oc::sensors::data::Magnetometer::mX)
        .def_readonly("mY",        &sl_oc::sensors::data::Magnetometer::mY)
        .def_readonly("mZ",        &sl_oc::sensors::data::Magnetometer::mZ)
          .def_property_readonly("valid", [](const sl_oc::sensors::data::Magnetometer &data) {
               return static_cast<int>(data.valid);
          });
    // <---- Bind Magnetometer data struct

    // ----> Bind Environment data struct
    py::class_<sl_oc::sensors::data::Environment>(m, "EnvironmentData")
        .def_readonly("timestamp", &sl_oc::sensors::data::Environment::timestamp)
        .def_readonly("press",     &sl_oc::sensors::data::Environment::press)
        .def_readonly("temp",      &sl_oc::sensors::data::Environment::temp)
        .def_readonly("humid",     &sl_oc::sensors::data::Environment::humid)
          .def_property_readonly("valid", [](const sl_oc::sensors::data::Environment &data) {
               return static_cast<int>(data.valid);
          });
    // <---- Bind Environment data struct

    // ----> Bind Temperature data struct
    py::class_<sl_oc::sensors::data::Temperature>(m, "TemperatureData")
        .def_readonly("timestamp",   &sl_oc::sensors::data::Temperature::timestamp)
        .def_readonly("temp_left",   &sl_oc::sensors::data::Temperature::temp_left)
        .def_readonly("temp_right",  &sl_oc::sensors::data::Temperature::temp_right)
          .def_property_readonly("valid", [](const sl_oc::sensors::data::Temperature &data) {
               return static_cast<int>(data.valid);
          });
    // <---- Bind Temperature data struct

    // ----> Bind SensorCapture class
    py::class_<sl_oc::sensors::SensorCapture>(m, "SensorCapture")
        .def(py::init<sl_oc::VERBOSITY>(),
             py::arg("verbose") = sl_oc::VERBOSITY::INFO)
        .def("get_device_list",
             &sl_oc::sensors::SensorCapture::getDeviceList,
             py::arg("refresh") = false)
        .def("initialize_sensors",
             &sl_oc::sensors::SensorCapture::initializeSensors,
             py::arg("device_id"))
        .def("get_serial_number",
             &sl_oc::sensors::SensorCapture::getSerialNumber)
        .def("get_firmware_version",
             // getFirmwareVersion uses output params, so wrap it into a tuple
             [](sl_oc::sensors::SensorCapture &s) {
                 uint16_t major, minor;
                 s.getFirmwareVersion(major, minor);
                 return py::make_tuple(major, minor);
             })
        .def("get_last_imu_data",
             &sl_oc::sensors::SensorCapture::getLastIMUData,
             py::arg("timeout_usec") = 5000)
        .def("get_last_magnetometer_data",
             &sl_oc::sensors::SensorCapture::getLastMagnetometerData,
             py::arg("timeout_usec") = 100)
        .def("get_last_environment_data",
             &sl_oc::sensors::SensorCapture::getLastEnvironmentData,
             py::arg("timeout_usec") = 100)
        .def("get_last_camera_temperature_data",
             &sl_oc::sensors::SensorCapture::getLastCameraTemperatureData,
             py::arg("timeout_usec") = 100);
    // <---- Bind SensorCapture class
    // ----> Expose NEW_VAL sentinel constants for validity checks
    m.attr("IMU_NEW_VAL")  = static_cast<int>(sl_oc::sensors::data::Imu::NEW_VAL);
    m.attr("MAG_NEW_VAL")  = static_cast<int>(sl_oc::sensors::data::Magnetometer::NEW_VAL);
    m.attr("ENV_NEW_VAL")  = static_cast<int>(sl_oc::sensors::data::Environment::NEW_VAL);
    m.attr("TEMP_NEW_VAL") = static_cast<int>(sl_oc::sensors::data::Temperature::NEW_VAL);
    // <---- Expose NEW_VAL sentinel constants
}
