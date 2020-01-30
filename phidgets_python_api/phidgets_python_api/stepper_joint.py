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
from phidgets_python_api.stepper import Stepper, StepperInfo
from phidgets_python_api.digital_input import DigitalInput, DigitalInputInfo

class StepperJointInfo():
    def __init__(self):
        self.stepper_info = StepperInfo()
        self.home_switch_info = DigitalInputInfo()
        self.limit_switch_info = None
        self.home_velocity_limit = 1000
        self.home_target_position = -10000
        self.deactivate_home_switch_target_position = 200

class StepperJoint:
    def __init__(self, stepper_joint_info, name, logger):
        self.stepper_joint_info = stepper_joint_info
        self.name = name
        self.logger = logger

        self.stepper = Stepper(self.stepper_joint_info.stepper_info, self.name + '_stepper', self.logger)

        self.home_switch = DigitalInput(self.stepper_joint_info.home_switch_info, self.name + '_home_switch', self.logger)
        self.home_switch.set_on_state_change_handler(self._home_switch_handler)

        if self.stepper_joint_info.limit_switch_info is not None:
            self.limit_switch = DigitalInput(self.stepper_joint_info.limit_switch_info, self.name + '_limit_switch', self.logger)
            self.set_limit_switch_handler_to_disabled()
        else:
            self.limit_switch = None

        self.homed = False
        self.homing = False

    def open(self):
        self.stepper.open()
        self.home_switch.open()
        if self.limit_switch is not None:
            self.limit_switch.open()

    def close(self):
        self.stepper.close()
        self.home_switch.close()
        if self.limit_switch is not None:
            self.limit_switch.close()

    def has_handle(self, handle):
        if self.limit_switch is not None:
            if self.limit_switch.has_handle(handle):
                return True
        return self.stepper.has_handle(handle) or self.home_switch.has_handle(handle)

    def set_on_attach_handler(self, on_attach_handler):
        self.stepper.set_on_attach_handler(on_attach_handler)
        self.home_switch.set_on_attach_handler(on_attach_handler)
        if self.limit_switch is not None:
            self.limit_switch.set_on_attach_handler(on_attach_handler)

    def _on_attach_handler(self, handle):
        if self.stepper.has_handle(handle):
            self.stepper._on_attach_handler(handle)
        elif self.home_switch.has_handle(handle):
            self.home_switch._on_attach_handler(handle)
        elif self.limit_switch.has_handle(handle):
            self.limit_switch._on_attach_handler(handle)

    def is_attached(self):
        if self.limit_switch is not None:
            return self.stepper.is_attached() and self.home_switch.is_attached() and self.limit_switch.is_attached()
        else:
            return self.stepper.is_attached() and self.home_switch.is_attached()

    def home(self):
        self.homed = False
        self.homing = True
        self.stepper.set_velocity_limit(self.stepper_joint_info.home_velocity_limit)
        if not self.home_switch.is_active():
            self.stepper.set_target_position(self.stepper_joint_info.home_target_position)
        else:
            self.stepper.set_target_position(self.stepper_joint_info.deactivate_home_switch_target_position)
            self.home()

    def _home_switch_handler(self, handle, state):
        if self.home_switch.is_active():
            self.homed = True
            self.homing = False
            self.stepper.stop()
            self.stepper.add_position_offset(-self.stepper.get_position())
            self.stepper.set_target_position(0.0)
            self.stepper.set_velocity_limit(self.stepper_joint_info.stepper_info.velocity_limit)

    def _stop_handler(self, handle, state):
        if (self.limit_switch is not None) and self.limit_switch.is_active():
            self.stepper.stop()

    def set_limit_switch_handler(self, limit_switch_handler):
        if self.limit_switch is not None:
            self.limit_switch.set_on_state_change_handler(limit_switch_handler)

    def set_limit_switch_handler_to_stop(self):
        if self.limit_switch is not None:
            self.limit_switch.set_on_state_change_handler(self._stop_handler)

    def set_limit_switch_handler_to_disabled(self):
        if self.limit_switch is not None:
            self.limit_switch.set_on_state_change_handler(None)
