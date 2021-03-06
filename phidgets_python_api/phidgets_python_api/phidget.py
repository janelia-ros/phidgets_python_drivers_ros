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

import Phidget22
from Phidget22.PhidgetException import *

class PhidgetInfo():
    def __init__(self):
        self.serial_number = Phidget22.Phidget.Phidget.ANY_SERIAL_NUMBER
        self.label = Phidget22.Phidget.Phidget.ANY_LABEL
        self.channel = Phidget22.Phidget.Phidget.ANY_CHANNEL
        self.hub_port = Phidget22.Phidget.Phidget.ANY_HUB_PORT
        self.is_hub_port_device = False

class Phidget:
    def __init__(self, phidget_info, name, logger):
        self.phidget_info = phidget_info
        self.name = name
        self.logger = logger

        self._set_handle_and_on_attach_handler(None)

    def _set_handle_and_on_attach_handler(self, phidget_handle):
        self._phidget_handle = phidget_handle
        self.set_on_attach_handler(self._on_attach_handler)

    def _on_attach_handler(self, handle):
        self.phidget_info.serial_number = self._phidget_handle.getDeviceSerialNumber()
        self.phidget_info.label = self._phidget_handle.getDeviceLabel()
        self.phidget_info.channel = self._phidget_handle.getChannel()
        self.phidget_info.hub_port = self._phidget_handle.getHubPort()
        self.phidget_info.is_hub_port_device = self._phidget_handle.getIsHubPortDevice()

        if self.phidget_info.label:
            msg = '{0} -> label: {1.label}, hub_port: {1.hub_port}'
        else:
            msg = '{0} -> serial_number: {1.serial_number}, hub_port: {1.hub_port}'
        msg = msg.format(self.name, self.phidget_info)
        self.logger.info(msg)

    def open(self):
        self._phidget_handle.setDeviceSerialNumber(self.phidget_info.serial_number)
        if self.phidget_info.label:
            self._phidget_handle.setDeviceLabel(self.phidget_info.label)
        self._phidget_handle.setChannel(self.phidget_info.channel)
        self._phidget_handle.setHubPort(self.phidget_info.hub_port)
        self._phidget_handle.setIsHubPortDevice(self.phidget_info.is_hub_port_device)

        self._phidget_handle.open()

    def close(self):
        if self._phidget_handle is not None:
            self._phidget_handle.close()

    def is_attached(self):
        if self._phidget_handle is None:
            return False
        return self._phidget_handle.getAttached()

    # def on_attach_handler(self, handle):
    def set_on_attach_handler(self, on_attach_handler):
        if self._phidget_handle is not None:
            self._phidget_handle.setOnAttachHandler(on_attach_handler)

    # def on_detach_handler(self, handle):
    def set_on_detach_handler(self, on_detach_handler):
        if self._phidget_handle is not None:
            self._phidget_handle.setOnDetachHandler(on_detach_handler)

    # def on_error_handler(self, handle, code, description):
    def set_on_error_handler(self, on_error_handler):
        if self._phidget_handle is not None:
            self._phidget_handle.setOnErrorHandler(on_error_handler)
