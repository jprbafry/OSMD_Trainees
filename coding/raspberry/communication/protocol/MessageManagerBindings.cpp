#include "MessageManager.h"
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

PYBIND11_MODULE(ComsModule, mm){
  mm.doc() = "Python binding for messagemanager class";

  py::class_<MessageManager::Sensors>(mm, "Sensors")
    .def(py::init<>())
    .def_property_readonly("motor_encoders", [](const MessageManager::Sensors &s){
        return py::array_t<uint16_t>({4}, s.motor_encoders);
    })
    .def_property_readonly("home_switches", [](const MessageManager::Sensors &s){
        return py::array_t<bool>({4}, s.home_switches);
    })
    .def_property_readonly("potentiometers", [](const MessageManager::Sensors &s){
        return py::array_t<uint16_t>({2}, s.potentiometers);
    })
    .def_property_readonly("ref_diode",  [](const MessageManager::Sensors &s){
        return s.ref_diode;
    })
    .def_property_readonly("temp_sensor",  [](const MessageManager::Sensors &s){
        return s.temp_sensor;
    })
    .def_property_readonly("imu", [](const MessageManager::Sensors &s){
        return py::array_t<float>({6}, s.imu);
    });

  py::class_<MessageManager>(mm, "MessageManager") 
    .def(py::init<>())

// SETTERS
    .def("setMotorEncoder", [](MessageManager &m, py::list lst) {
            if (py::len(lst) != 4) throw std::runtime_error("Expected 4 elements");
            uint16_t tmp[4];
            for (int i=0; i<4; i++)
                tmp[i] = lst[i].cast<uint16_t>();
            m.setMotorEncoder(tmp);
    })
    .def("setHomeSwitches", [](MessageManager &m, py::list lst){
         if (py::len(lst) != 4) throw std::runtime_error("Expected 4 elements");
            bool tmp[4];
            for (int i=0; i<4; i++)
                tmp[i] = lst[i].cast<bool>();
            m.setHomeSwitches(tmp);
    })
    .def("setPotentioMeters", [](MessageManager &m, py::list lst){
         if (py::len(lst) != 2) throw std::runtime_error("Expected 2 elements");
            uint16_t tmp[2];
            for (int i=0; i<2; i++)
                tmp[i] = lst[i].cast<uint16_t>();
            m.setPotentiometers(tmp);
    })
    .def("setRefDiode", &MessageManager::setRefDiode)
    .def("setTempSensor", &MessageManager::setTempSensor)
    .def("setImu", [](MessageManager &m, py::list lst) {
            if (lst.size() != 6) throw std::runtime_error("Expected 6 elements");
            float tmp[6];
            for (int i=0; i<6; i++)
                tmp[i] = lst[i].cast<float>();
            m.setImu(tmp);
    })

// VARIABLES


 /**
  * THIS EXPORTS THE PAYLOAD SUCCESSFULLY, HOWEVER IT KEEPS THE SIZE CONSTANT, FILLS THE NON POPULATED FIELDS WITH 0s
  */

    .def_property_readonly("payload", [](MessageManager &m){
        return py::array(
            py::buffer_info(
                m.payload,                                      //pointer
                sizeof(uint8_t),                                //item size
                py::format_descriptor<uint8_t>::value,          //format
                1,                                              //ndim
                {64},                                           //shape
                {sizeof(uint8_t)}                               //strides
            )
        );
    })

    .def_readwrite("mask", &MessageManager::mask)
    
// OTHER FUNCTIONS
    .def("getPayload", [](const MessageManager &m){
        return py::array_t<uint8_t>({64}, m.payload);
    })
    .def("getSensors", &MessageManager::getSensors, py::return_value_policy::reference)
    .def("packPayload", &MessageManager::packPayload)
    .def("fillPayload", &MessageManager::fillPayload)
    .def("loadData", &MessageManager::loadData);
  };