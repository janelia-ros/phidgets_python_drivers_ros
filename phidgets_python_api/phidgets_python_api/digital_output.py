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
import Phidget22.Devices.DigitalOutput

from phidgets_python_api.phidget import Phidget, PhidgetInfo

class DigitalOutputInfo():
    def __init__(self):
        self.phidget_info = PhidgetInfo()
        self.phidget_info.is_hub_port_device = True
        self.active_high = True

class DigitalOutput(Phidget):
    def __init__(self, digital_output_info, name, logger):
        super().__init__(digital_output_info.phidget_info, name, logger)
        self.digital_output_info = digital_output_info

        self._set_handle_and_on_attach_handler(Phidget22.Devices.DigitalOutput.DigitalOutput())

    def _set_handle_and_on_attach_handler(self, digital_output_handle):
        super()._set_handle_and_on_attach_handler(digital_output_handle)
        self._digital_output_handle = digital_output_handle
        self.set_on_attach_handler(self._on_attach_handler)

    def _on_attach_handler(self, handle):
        super()._on_attach_handler(handle)

    def close(self):
        super().close()

    def has_handle(self, handle):
        return self._digital_output_handle == handle

    def get_state(self):
        return self._digital_output_handle.getState()

    def set_state(self, state):
        self._digital_output_handle.setState(state)

    def is_active(self):
        if self.digital_output_info.active_high:
            return self.get_state()
        else:
            return not self.get_state()

    def activate(self):
        if self.digital_output_info.active_high:
            return self.set_state(True)
        else:
            return not self.set_state(False)

    def deactivate(self):
        if self.digital_output_info.active_high:
            return self.set_state(False)
        else:
            return not self.set_state(True)
