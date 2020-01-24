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

class StepperJoint:
    def __init__(self, stepper_joint_info, name, logger):
        self.stepper_joint_info = stepper_joint_info
        self.name = name
        self.logger = logger

        self._setup_stepper_joint()

    def _setup_stepper_joint(self):
        try:
            self.stepper = Stepper(self.stepper_joint_info.stepper_info, self.name + '_stepper', self.logger)
            self.home_switch = DigitalInput(self.stepper_joint_info.home_switch_info, self.name + '_home_switch', self.logger)
        except PhidgetException as e:
            self.stepper.close()
            self.home_switch.close()
            raise

        if self.stepper_joint_info.limit_switch_info is not None:
            try:
                self.limit_switch = DigitalInput(self.stepper_joint_info.limit_switch_info, self.name + '_limit_switch', self.logger)
            except PhidgetException as e:
                self.limit_switch = None

        self.home_switch.set_on_state_change_handler(self._home_switch_handler)
        self.homed = False
        self.homing = False
        if self.limit_switch is not None:
            self.limit_switch.set_on_state_change_handler(self._limit_switch_handler)

    def close(self):
        self.stepper.close()
        self.home_switch.close()
        if self.limit_switch is not None:
            self.limit_switch.close()

    def home(self):
        if not self.home_switch.is_active():
            self.homed = False
            self.homing = True
            self.stepper.set_velocity_limit(self.stepper_joint_info.home_velocity_limit)
            self.stepper.set_target_position(self.stepper_joint_info.home_target_position)
        else:
            self._home_switch_handler(self.home_switch, False)

    def _home_switch_handler(self, handle, state):
        if self.home_switch.is_active():
            self.stepper.set_velocity_limit(0.0)
            self.stepper.add_position_offset(-self.stepper.get_position())
            self.stepper.set_target_position(0.0)
            self.stepper.set_velocity_limit(self.stepper_joint_info.stepper_info.velocity_limit)
            self.homed = True
            self.homing = False
            self.logger.info('{0} homed'.format(self.name))

    def _limit_switch_handler(self, handle, state):
        if (self.limit_switch is not None) and self.limit_switch.is_active():
            self.stepper.set_velocity_limit(0.0)
            self.logger.info('{0} limit switch is active'.format(self.name))
