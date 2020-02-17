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
import Phidget22.Devices.Stepper

from phidgets_python_api.phidget import Phidget, PhidgetInfo

class StepperInfo():
    def __init__(self):
        self.phidget_info = PhidgetInfo()
        self.data_interval = 100
        self.rescale_factor = 1.0
        self.acceleration = 10000
        self.velocity_limit = 10000
        self.home_velocity_limit = 1000
        self.home_target_position = -10000
        self.current_limit = 0.1
        self.holding_current_limit = 0.0
        self.invert_direction = False

class Stepper(Phidget):
    def __init__(self, name, logger, stepper_info):
        super().__init__(name, logger, stepper_info.phidget_info)
        self.stepper_info = stepper_info

        self.set_handle(Phidget22.Devices.Stepper.Stepper())
        self.set_on_attach_handler(self._on_attach_handler)

        self._step_control_mode = True
        self._direction = 1

    def set_handle(self, stepper_handle):
        super().set_handle(stepper_handle)
        self._stepper_handle = stepper_handle

    def has_handle(self, handle):
        return self._stepper_handle == handle

    def _on_attach_handler(self, handle):
        super()._on_attach_handler(handle)
        self.set_data_interval(self.stepper_info.data_interval)
        self.set_rescale_factor(self.stepper_info.rescale_factor)
        self.set_acceleration(self.stepper_info.acceleration)
        self.set_current_limit(self.stepper_info.current_limit)
        self.set_holding_current_limit(self.stepper_info.holding_current_limit)
        self.set_velocity_limit(self.stepper_info.velocity_limit)
        if self.stepper_info.invert_direction:
            self._direction = -1

        self.enable()

    def close(self):
        self.set_on_position_change_handler(None)
        self.set_on_velocity_change_handler(None)
        self.set_on_stopped_handler(None)
        self.disable()
        super().close()

    # def on_position_change_handler(self, handle, position):
    def set_on_position_change_handler(self, on_position_change_handler):
        self._stepper_handle.setOnPositionChangeHandler(on_position_change_handler)

    # def on_velocity_change_handler(self, handle, velocity):
    def set_on_velocity_change_handler(self, on_velocity_change_handler):
        self._stepper_handle.setOnVelocityChangeHandler(on_velocity_change_handler)

    # def on_stopped_handler(self, handle):
    def set_on_stopped_handler(self, on_stopped_handler):
        self._stepper_handle.setOnStoppedHandler(on_stopped_handler)

    def get_acceleration(self):
        return self._stepper_handle.getAcceleration()

    def set_acceleration(self, acceleration):
        self._stepper_handle.setAcceleration(acceleration)

    def get_min_acceleration(self):
        return self._stepper_handle.getMinAcceleration()

    def get_max_acceleration(self):
        return self._stepper_handle.getMaxAcceleration()

    def in_step_control_mode(self):
        return self._step_control_mode

    def set_step_control_mode(self):
        self._stepper_handle.setControlMode(Phidget22.Devices.Stepper.StepperControlMode.CONTROL_MODE_STEP)
        self._step_control_mode = True

    def set_velocity_control_mode(self):
        self._stepper_handle.setControlMode(Phidget22.Devices.Stepper.StepperControlMode.CONTROL_MODE_RUN)
        self._step_control_mode = False

    def get_current_limit(self):
        return self._stepper_handle.getCurrentLimit()

    def set_current_limit(self, current_limit):
        self._stepper_handle.setCurrentLimit(current_limit)

    def get_min_current_limit(self):
        return self._stepper_handle.getMinCurrentLimit()

    def get_max_current_limit(self):
        return self._stepper_handle.getMinCurrentLimit()

    def get_data_interval(self):
        return self._stepper_handle.getDataInterval()

    def set_data_interval(self, data_interval):
        self._stepper_handle.setDataInterval(data_interval)

    def get_min_data_interval(self):
        return self._stepper_handle.getMinDataInterval()

    def get_max_data_interval(self):
        return self._stepper_handle.getMaxDataInterval()

    def enable(self):
        self._stepper_handle.setEngaged(True)

    def disable(self):
        self._stepper_handle.setEngaged(False)

    def is_enabled(self):
        return self._stepper_handle.getEngaged()

    def get_holding_current_limit(self):
        return self._stepper_handle.getHoldingCurrentLimit()

    def set_holding_current_limit(self, holding_current_limit):
        self._stepper_handle.setHoldingCurrentLimit(holding_current_limit)

    def is_moving(self):
        return self._stepper_handle.getIsMoving()

    def get_position(self):
        return self._direction * self._stepper_handle.getPosition()

    def add_position_offset(self, position_offset):
        self._stepper_handle.addPositionOffset(self._direction * position_offset)

    def get_rescale_factor(self):
        return self._stepper_handle.getRescaleFactor()

    def set_rescale_factor(self, rescale_factor):
        self._stepper_handle.setRescaleFactor(rescale_factor)

    def get_target_position(self):
        return self._direction * self._stepper_handle.getTargetPosition()

    def set_target_position(self, target_position):
        if self.in_step_control_mode():
            self._stepper_handle.setTargetPosition(self._direction * target_position)

    def get_velocity(self):
        return self._direction * self._stepper_handle.getVelocity()

    def set_velocity_limit(self, velocity_limit):
        if self.in_step_control_mode():
            self._stepper_handle.setVelocityLimit(abs(velocity_limit))
        else:
            self._stepper_handle.setVelocityLimit(self._direction * velocity_limit)

    def get_min_velocity_limit(self):
        return self._stepper_handle.getMinVelocityLimit()

    def get_max_velocity_limit(self):
        return self._stepper_handle.getMaxVelocityLimit()

    def stop(self):
        self.set_velocity_limit(0.0)
