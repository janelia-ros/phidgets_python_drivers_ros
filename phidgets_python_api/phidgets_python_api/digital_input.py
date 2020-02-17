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
import Phidget22.Devices.DigitalInput

from phidgets_python_api.phidget import Phidget, PhidgetInfo

class DigitalInputInfo():
    def __init__(self):
        self.phidget_info = PhidgetInfo()
        self.phidget_info.is_hub_port_device = True
        self.active_low = True

class DigitalInput(Phidget):
    def __init__(self, name, logger, digital_input_info):
        super().__init__(name, logger, digital_input_info.phidget_info)
        self.digital_input_info = digital_input_info

        self.set_handle(Phidget22.Devices.DigitalInput.DigitalInput())
        self.set_on_attach_handler(self._on_attach_handler)

    def set_handle(self, digital_input_handle):
        super().set_handle(digital_input_handle)
        self._digital_input_handle = digital_input_handle

    def has_handle(self, handle):
        return self._digital_input_handle == handle

    def _on_attach_handler(self, handle):
        super()._on_attach_handler(handle)

    def close(self):
        self.set_on_state_change_handler(None)
        super().close()

    # def on_state_change_handler(self, handle, state):
    def set_on_state_change_handler(self, on_state_change_handler):
        self._digital_input_handle.setOnStateChangeHandler(on_state_change_handler)

    def get_state(self):
        return self._digital_input_handle.getState()

    def is_active(self):
        if self.digital_input_info.active_low:
            return self.get_state()
        else:
            return not self.get_state()
