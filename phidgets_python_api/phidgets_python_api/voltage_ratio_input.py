# Copyright (c) 2020, Howard Hughes Medical Institute
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from Phidget22.PhidgetException import *
import Phidget22
import Phidget22.Devices.VoltageRatioInput

from phidgets_python_api.phidget import Phidget, PhidgetInfo

class VoltageRatioInputInfo():
    def __init__(self):
        self.phidget_info = PhidgetInfo()
        self.bridge_gain = Phidget22.Devices.VoltageRatioInput.BridgeGain.BRIDGE_GAIN_1
        self.data_interval = 100
        self.sensor_type = Phidget22.Devices.VoltageRatioInput.VoltageRatioSensorType.SENSOR_TYPE_VOLTAGERATIO
        self.sensor_value_change_trigger = None
        self.voltage_ratio_change_trigger = None

class VoltageRatioInput(Phidget):
    def __init__(self, voltage_ratio_input_info, name, logger):
        super().__init__(voltage_ratio_input_info.phidget_info, name, logger)
        self.voltage_ratio_input_info = voltage_ratio_input_info

        self._set_handle_and_on_attach_handler(Phidget22.Devices.VoltageRatioInput.VoltageRatioInput())

    def _set_handle_and_on_attach_handler(self, voltage_ratio_input_handle):
        super()._set_handle_and_on_attach_handler(voltage_ratio_input_handle)
        self._voltage_ratio_input_handle = voltage_ratio_input_handle
        self.set_on_attach_handler(self._on_attach_handler)

    def _on_attach_handler(self, handle):
        super()._on_attach_handler(handle)
        self.set_bridge_gain(self.voltage_ratio_input_info.bridge_gain)
        self.set_data_interval(self.voltage_ratio_input_info.data_interval)
        # self.set_sensor_type(self.voltage_ratio_input_info.sensor_type)
        if self.voltage_ratio_input_info.sensor_value_change_trigger:
            self.set_sensor_value_change_trigger(self.voltage_ratio_input_info.sensor_value_change_trigger)
        if self.voltage_ratio_input_info.voltage_ratio_change_trigger:
            self.set_voltage_ratio_change_trigger(self.voltage_ratio_input_info.voltage_ratio_change_trigger)

    def close(self):
        self.set_on_sensor_change_handler(None)
        self.set_on_voltage_ratio_change_handler(None)
        super().close()

    def has_handle(self, handle):
        return self._voltage_ratio_input_handle == handle

    # def on_sensor_change_handler(self, handle, sensor_value, sensor_unit):
    def set_on_sensor_change_handler(self, on_sensor_change_handler):
        self._voltage_ratio_input_handle.setOnSensorChangeHandler(on_sensor_change_handler)

    # def on_voltage_ratio_change_handler(self, handle, voltage_ratio):
    def set_on_voltage_ratio_change_handler(self, on_voltage_ratio_change_handler):
        self._voltage_ratio_input_handle.setOnVoltageRatioChangeHandler(on_voltage_ratio_change_handler)

    def enable(self):
        self._voltage_ratio_input_handle.setBridgeEnabled(True)

    def disable(self):
        self._voltage_ratio_input_handle.setBridgeEnabled(False)

    def is_enabled(self):
        return self._voltage_ratio_input_handle.getBridgeEnabled()

    def set_bridge_gain(self, bridge_gain):
        self._voltage_ratio_input_handle.setBridgeGain(bridge_gain)

    def get_bridge_gain(self):
        return self._voltage_ratio_input_handle.getBridgeGain()

    def get_data_interval(self):
        return self._voltage_ratio_input_handle.getDataInterval()

    def set_data_interval(self, data_interval):
        self._voltage_ratio_input_handle.setDataInterval(data_interval)

    def get_min_data_interval(self):
        return self._voltage_ratio_input_handle.getMinDataInterval()

    def get_max_data_interval(self):
        return self._voltage_ratio_input_handle.getMaxDataInterval()

    def get_sensor_type(self):
        return self._voltage_ratio_input_handle.getSensorType()

    def set_sensor_type(self, sensor_type):
        self._voltage_ratio_input_handle.setSensorType(sensor_type)

    def get_sensor_unit(self):
        return self._voltage_ratio_input_handle.getSensorUnit()

    def get_sensor_value(self):
        return self._voltage_ratio_input_handle.getSensorValue()

    def get_sensor_value_change_trigger(self):
        return self._voltage_ratio_input_handle.getSensorValueChangeTrigger()

    def set_sensor_value_change_trigger(self, sensor_value_change_trigger):
        self._voltage_ratio_input_handle.setSensorValueChangeTrigger(sensor_value_change_trigger)

    def get_voltage_ratio(self):
        return self._voltage_ratio_input_handle.getVoltageRatio()

    def get_min_voltage_ratio(self):
        return self._voltage_ratio_input_handle.getMinVoltageRatio()

    def get_max_voltage_ratio(self):
        return self._voltage_ratio_input_handle.getMaxVoltageRatio()

    def get_voltage_ratio_change_trigger(self):
        return self._voltage_ratio_input_handle.getVoltageRatioChangeTrigger()

    def set_voltage_ratio_change_trigger(self, voltage_ratio_change_trigger):
        self._voltage_ratio_input_handle.setVoltageRatioChangeTrigger(voltage_ratio_change_trigger)

    def get_min_voltage_ratio_change_trigger(self):
        return self._voltage_ratio_input_handle.getMinVoltageRatioChangeTrigger()

    def get_max_voltage_ratio_change_trigger(self):
        return self._voltage_ratio_input_handle.getMaxVoltageRatioChangeTrigger()
