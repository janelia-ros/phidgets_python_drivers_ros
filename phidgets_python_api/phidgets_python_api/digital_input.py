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

import .PhidgetHelperFunctions

from phidget_python_api.phidget import Phidget, ChannelInfo

class DigitalInputInfo():
    def __init__(self):
        self.channel_info = ChannelInfo()
        self.channel_info.is_hub_port_device = True

class DigitalInput(Phidget):
    def __init__(self, digital_input_info):
        super().__init__(digital_input_info.channel_info)
        self._digital_input_info = digital_input_info

        try:
            self._handle = Phidget22.Devices.DigitalInput()
        except PhidgetException as e:
            DisplayError(e)
            raise

        open_wait_for_attachment(self._handle)
        _setup()

    def _setup(self):
        pass

    def close(self):
        self.set_on_state_change_handler(None)
        super().close(self._handle)

    # void onStateChange(self, state)
    def set_on_state_change_handler(self, on_state_change_handler):
        self._handle.setOnStateChangeHandler(on_state_change_handler)

    def get_state(self):
        return self._handle.getState()
